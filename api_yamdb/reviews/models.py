from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year

username_validator = UnicodeUsernameValidator()

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель управления пользователями."""

    username = models.CharField(
        'Никнейм',
        max_length=150,
        unique=True,
        validators=(username_validator, validate_username),
    )
    email = models.EmailField(
        'почта',
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
        blank=True,
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Группа пользователей',
        max_length=255,
        choices=CHOICES,
        default=USER,
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=True,
        default='***',
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(
        verbose_name='Идентификатор', max_length=50, unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(
        verbose_name='Идентификатор', max_length=50, unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    """Модель тайтлов."""

    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.IntegerField(
        verbose_name='Дата выхода', validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг', null=True, default=None
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    """Модель промежуточной таблицы
    жанры-произведения."""

    title = models.ForeignKey(
        Title, verbose_name='Произведение', on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, verbose_name='Жанр', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Ревью'


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.author
