import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import Member
from main.forms import RegistrationForm, LoginForm, ProjectForm, ProjectFilesForm, ServiceForm
from accounts.admin import UserCreationForm
from django.core.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from service.models import *
from orders.models import *
from coupons.models import *
from shop.models import Stock
from orders.forms import OrderCreateForm
from decimal import Decimal
from django.views import generic


@login_required(login_url="main:login")
def main_view(request, *args, **kwargs):
    users = Member.objects.all()
    projects = Project.objects.all()
    spent = sum(int(project.spent.amount) for project in projects)
    budget = sum(int(project.budget.amount) for project in projects)
    x = spent / budget * 100
    rate = float("{:.2f}".format(x))
    context = {
        "users": users,
        "spent": spent,
        "currency": "Ush",
        "rate": rate,
        "projects": projects,
        "active": "home",
        "title": "Deut818 System Administration",
    }
    return render(request, "main/index.html", context)

def register_view(request, *args, **kwargs):
    form = RegistrationForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            
            return redirect('main:login')
    else:
        form = RegistrationForm(request.GET)
    context= {
        "form": form,
        "active": "register",
        "title": "DSA | Register new Membership"
    }
    return render(request, "main/pages/auth/register.html", context)

def login_view(request, *args, **kwargs):
    form = LoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('/')
            else:
                # Return an 'invalid login' error message.
                raise ValidationError("Email or Password is incorrect")
    context = {
        "active": "login",
        "form": form,
        "title": "DSA | Login to your dashboard"
    }
    return render(request, "main/pages/auth/login.html", context)


def forgot_password_view(request, *args, **kwargs):
    context = {
        "title": "DSA | Forgot password",
        "active": "forgot-password",
    }
    return render(request, "main/pages/auth/forgot-password.html", context)

@login_required(login_url='main:login')
def users_view(request, *args, **kwargs):
    users = Member.objects.all()
    context = {
        "users": users,
        "title": "DSA | Members",
        "active": "users",
    }
    return render(request, "main/pages/content/users.html", context)
    
@login_required(login_url='main:login')
def user_profile_view(request):
    context = {
        "active": "profile",
        "title": "DSA | Members",
    }
    return render(request, "main/pages/content/profile.html", context)
    
@login_required(login_url='main:login')
def dashboard_view(request, *args, **kwargs):
    projects = Project.objects.all()
    services = Service.objects.all()
    clients = Client.objects.all()
    members = Member.objects.all()
    spent = sum(int(project.spent.amount) for project in projects)
    budget = sum(int(project.budget.amount) for project in projects)
    x = spent / budget * 100
    rate = float("{:.2f}".format(x))

    context = {
        
        "title": "DSA | Dashboard",
        "projects": projects,
        "services": services,
        "clients": clients,
        "members": members,
        "rate": rate,
        "spent": spent,
        "budget": budget,
        "active": "dashboard",
    }
    return render(request, "main/pages/content/dashboard.html", context)

# ****** PROJECTS ******* # 
@login_required(login_url='main:login')
def projects_view(request):
    projects = Project.objects.all()
    request.session['success'] = "";
    
    context = {
        "title": "DSA | Projects",
        "projects": projects,
        "breadcrub": "projects",
        "active": "projects",
    }
    return render(request, "main/pages/content/projects.html", context)

@login_required(login_url='main:login')
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    context = {
        "title": "DSA | Project Detail",
        "project": project,
        "active": "project_detail"
    }
    return render(request, "main/pages/content/project_detail.html", context)

@login_required(login_url='main:login')
def projects_add(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            success = f"The project {cd['title']} has been added successfully"
            form.save()
            p = Project.objects.latest('id')
            return redirect(f"/project/{p.id}")
            
    else:
        form = ProjectForm()

    context = {
        "form": form,
        "title": "DSA | Add Project",
        "active": "projects_add"
    }

    return render(request, "main/pages/content/projects_add.html", context)

@login_required(login_url='main:login')
def order_add(request, *args, **kwargs):
    
    if request.method == "POST": 
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.save()
            order = Order.objects.latest('id')
            qty = order.quantity
            p = order.product
            stock = Stock.objects.get(product=p)
            x = stock.ammount - qty
            stock.ammount = x
            stock.save()

            # TODO: Calculate the total ammount using javascript.



    context = {

        "title": "DSA | Make an Order",
    }
    return render(request, "main:order", context)

class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main/pages/content/project_update_form.html'


@login_required(login_url='main:login')
def project_files_add_view(request, id):
    p = Project.objects.get(id=id)
    img = [".png", ".jpg", ".jpeg", ".gif", ".PNG", ".JPG", ".JPEG", ".GIF"]
    vid = [".mp4","webm", ".ogg"]
    pdf = ".pdf"
    doc = ".doc"
    ppt = ".ppt"
    com = [".zip", ".rar"]
    csv = ".csv"
    exc = ".xlsx"
    pub = ".pub"
    code = [".asp", ".aspx", ".axd", ".asx", ".asmx", ".ashx", ".cfm", ".yaws", ".htm", ".html", '.xhtml', '.shtml', '.jhtml', '.jsp', '.jspx', '.wss', '.do', '.action', '.pl', '.php', '.php4', '.php3', '.phtml', '.py', '.rb', '.rhtml', '.rss', '.xml', '.cgi', '.dll', '.fcgi', '.dart', '.iml', 'yaml', '.json', '.js', '.css', '.yaml', '.md']
    txt = ".txt"
    data = {
        'project': p
    }
    if request.method == "POST":
        form = ProjectFilesForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            f = ProjectFile.objects.latest('id')
            file_name = f.file.name
            file_extension = os.path.splitext(file_name)[1]
            f.extension = file_extension
            f.save()
            return redirect(f'/project/{cd["project"].id}')
            
    else:
        form = ProjectFilesForm(initial=data)

    context = {
        "form": form,
        "title": "DSA | Add Project Files",
        "png": ".png",
        "jpg": ".jpg",
        "gif": ".gif",
        "mp4": ".mp4",
        "mp3": ".mp3",
        "wav": ".wav",
        "webm": ".webm",
        "pdf": ".pdf",
        "doc": ".doc",
        "ppt": ".ppt",
        "zip": ".zip",
        "csv": ".csv",
        "exc": ".xlsx",
        "pub": ".pub",
        "txt": ".txt",
        "active": "project_files_add",
    }

    return render(request, "main/pages/content/project_files_add.html", context)


# *********************************************** SERVICES ************************************************* #

@login_required(login_url='main:login')
def services_view(request):
    services = Service.objects.all()
    request.session['success'] = "";
    
    context = {
        "title": "DSA | Services",
        "services": services,
        "active": "services"
    }
    return render(request, "main/pages/content/services/main.html", context)

@login_required(login_url='main:login')
def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    context = {
        "title": "DSA | Service Detail",
        "service": service,
        "active": "service_detail"
    }
    return render(request, "main/pages/content/services/detail.html", context)

@login_required(login_url='main:login')
def service_add(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            p = Service.objects.latest('id')
            return redirect(f"/service/{p.id}")
            
    else:
        form = ServiceForm()

    context = {
        "form": form,
        "title": "DSA | Add Service",
        "active": "services_add"
    }

    return render(request, "main/pages/content/services/add.html", context)


class ServiceUpdateView(generic.UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'main/pages/content/services/update_form.html'



# Chart Data API
class ChartData(APIView):
    def get(self, request, format=None):
        """
        Chart Data
        """
        projects = Project.objects.all().count()
        clients = Client.objects.all().count()
        members = Member.objects.all().count()
        services = Service.objects.all().count()
        labels = ["Projects", "Clients", "Members", "Services"]
        default_items = [projects, clients, members, services]
        data = {
            "default": default_items,
            "labels": labels,
        }
        return Response(data)

class ProjectChart(APIView):
    def get(self, request, format=None):
        jan = Project.objects.all().filter(started__month = 1).count()
        feb = Project.objects.all().filter(started__month = 2).count()
        mar = Project.objects.all().filter(started__month = 3).count()
        apr = Project.objects.all().filter(started__month = 4).count()
        may = Project.objects.all().filter(started__month = 5).count()
        jun = Project.objects.all().filter(started__month = 6).count()
        jul = Project.objects.all().filter(started__month = 7).count()
        aug = Project.objects.all().filter(started__month = 8).count()
        sep = Project.objects.all().filter(started__month = 9).count()
        octo = Project.objects.all().filter(started__month = 10).count()
        nov = Project.objects.all().filter(started__month = 11).count()
        dec = Project.objects.all().filter(started__month = 12).count()
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "sep", "Oct", "Nov", "Dec"]
        default_items = [jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec]

        data = {
            "default": default_items,
            "labels": labels,
        }
        return Response(data)