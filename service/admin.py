from django.contrib import admin
from service.models import Service, Project, Client, ProjectFile
# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "available"]

    search_fields = ('title',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "service", "client", "budget", "spent", "status", "duration", "started", "ended"]

    search_fields = ('title',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "tel", "email", "address"]

    search_fields = ('name',)

class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ["project", "name", "file", "extension"]

admin.site.register(ProjectFile, ProjectFileAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Service, ServiceAdmin)