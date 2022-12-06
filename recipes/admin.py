from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    ...

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published']




admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Recipe, RecipeAdmin)