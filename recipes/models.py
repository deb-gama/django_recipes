import string
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from random import choices, SystemRandom


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')',)
            )
        ).order_by('-id').select_related('category', 'author')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    # TODO arrumar o nome do field abaixo: prepAration
    preperation_time_unit = models.CharField(max_length=10)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=10)
    preparation_step = models.TextField()
    preparation_step_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        default=None
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        return super().save(*args, **kwargs)






