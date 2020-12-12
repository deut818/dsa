from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from main import views

app_name = "main"
urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('home', views.main_view, name="home"),
    path('register', views.register_view, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    path('forgot-password', views.forgot_password_view, name="forgot-password"),
    path('users', views.users_view, name="members"),
    path('profile', views.user_profile_view, name="profile"),
    path('projects', views.projects_view, name="projects"),
    path('projects/add', views.projects_add, name="projects_add"),
    path('project/<int:id>', views.project_detail, name='project_detail'),
    path('project/<int:id>/add/files', views.project_files_add_view, name='project_files_add'),
    path('services', views.services_view, name="services"),
    path('services/add', views.service_add, name="services_add"),
    path('service/<int:id>', views.service_detail, name='service_detail'),

    # RE_PATH URLs
    re_path(r'^project/edit/(?P<pk>\d+)/$', views.ProjectUpdateView.as_view(), name='project_update'),
    re_path(r'^service/edit/(?P<pk>\d+)/$', views.ServiceUpdateView.as_view(), name='service_update'),
    

    # API URLs
    path('api/chart/data', views.ChartData.as_view(), name="chart-data-api"),
    path('api/projects/data', views.ProjectChart.as_view(), name="project-api"),
]