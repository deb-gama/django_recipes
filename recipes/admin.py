from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    ...


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_published", "created_at"]
    list_display_links = ["title"]
    search_fields = ["id", "title", "description", "slug"]
    list_filter = ["category", "author", "is_published", "preparation_step_is_html"]
    list_per_page = 10
    list_editable = ["is_published"]
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
