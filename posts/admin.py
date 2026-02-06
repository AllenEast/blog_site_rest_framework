from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Post


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = '__all__'



class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'




@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    resource_classes = [PostResource]
    form = PostAdminForm

    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]

