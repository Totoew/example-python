from django.contrib import admin
from . import models
import csv
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages


def upload_csv(admin, request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Это не CSV файл!")
            return HttpResponseRedirect(request.path_info)

        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
        header = next(reader)  # Получаем заголовки
        model = admin.model

        # Создаем объекты модели из CSV
        for row in reader:
            obj_data = dict(zip(header, row))
            model.objects.create(**obj_data)

        messages.success(request, "Данные успешно загружены!")
        return HttpResponseRedirect(request.path_info)

    # Шаблон для загрузки
    return render(request, "admin/csv_upload.html", context={"model": admin.model})


class YearAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary', 'count', 'salary_vac', 'count_vac')
    list_editable = ('salary', 'count', 'salary_vac', 'count_vac')

    change_list_template = "admin/change_list_with_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv_view), name="upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        return upload_csv(self, request)


class AreaSalaryAdmin(admin.ModelAdmin):
    list_display = ('area', 'salary')
    list_editable = ('salary', )

    change_list_template = "admin/change_list_with_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv_view), name="upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        return upload_csv(self, request)


class AreaPartAdmin(admin.ModelAdmin):
    list_display = ('area', 'part')
    list_editable = ('part', )

    change_list_template = "admin/change_list_with_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv_view), name="upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        return upload_csv(self, request)


class YearSkillsAdmin(admin.ModelAdmin):
    list_display = ('year', ) + tuple(f'skill{i}' for i in range(1, 21))
    list_editable = tuple(f'skill{i}' for i in range(1, 21))

    change_list_template = "admin/change_list_with_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv_view), name="upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        return upload_csv(self, request)


class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    list_editable = ('image',)


admin.site.register(models.YearAnalytics, YearAnalyticsAdmin)
admin.site.register(models.AreaSalary, AreaSalaryAdmin)
admin.site.register(models.AreaPart, AreaPartAdmin)
admin.site.register(models.AreaSalaryVacancy, AreaSalaryAdmin)
admin.site.register(models.AreaPartVacancy, AreaPartAdmin)
admin.site.register(models.YearSkills, YearSkillsAdmin)
admin.site.register(models.YearSkillsVacancy, YearSkillsAdmin)
admin.site.register(models.ImageModel, ImageModelAdmin)
