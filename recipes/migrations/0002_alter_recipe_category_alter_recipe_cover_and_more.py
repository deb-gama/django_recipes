# Generated by Django 4.1.3 on 2022-12-11 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="recipes.category",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(blank=True, upload_to="recipes/covers/%Y/%m/%d/"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]
