from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify


User = get_user_model()


MAKET_RU = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
MAKET_EN = 'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA'


class Tag(models.Model):
    MEALS = (
        ('Завтрак', 'breakfast'),
        ('Обед', 'lunch'),
        ('Ужин', 'dinner'),
    )
    title = models.CharField(
        verbose_name='Название тега',
        max_length=100,
        unique=True,
        choices=MEALS
    )
    display_name = models.CharField(
        max_length=20,
        verbose_name='Имя тега в шаблоне',
        # default='Name'
    )
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет тега',
        default="Red"
    )

    def __str__(self):
        return f'{self.title}'


class Ingredient(models.Model):
    title = models.CharField(max_length=254)
    unit = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}, {self.unit}'

    class Meta:
        ordering = ('title', )
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class RecipeQuerySet(models.QuerySet):

    def with_is_favorite(self, user_id):
        return self.annotate(
            is_favorite=models.Exists(
                Favorite.objects.filter(
                    user_id=user_id,
                    recipe_id=models.OuterRef('pk'),
                ),
            ))


class Recipe(models.Model):
    title = models.CharField(
        max_length=254, verbose_name='Название рецепта'
        )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фото рецепта',
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    time_cooking = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )
    slug = models.SlugField(
        verbose_name='Ссылка на рецепт',
        unique=True, null=True, blank=True
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe',
        related_name='recipes',
        verbose_name='Тэг'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингридиент',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.title

    def text_trim(self):
        return u"%s..." % (self.text[:50],)

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        maket_ru = MAKET_RU
        maket_en = MAKET_EN
        self.slug = slugify(
            self.title.translate(
                str.maketrans(
                    maket_ru, maket_en
                )))
        return super(Recipe, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipes',
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тэг в рецепте'
        verbose_name_plural = 'Теги в рецептах'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор публикации'
    )

    def __str__(self):
        return f'{self.user} подписан на автора {self.author} '

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                '''
                Пользователь не может
                подписываться на самого себя
                '''
            )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow_user_author'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'Выбранный рецепт {self.recipe} в покупках у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_purchases_user_recipe'
            )
        ]
        verbose_name = 'Объект покупок'
        verbose_name_plural = 'Объекты покупок'
