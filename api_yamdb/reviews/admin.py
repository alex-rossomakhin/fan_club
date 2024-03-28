from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
    site=admin.sites.site,
)
class PostAdmin(admin.ModelAdmin):
    pass
