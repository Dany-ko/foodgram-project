from django.contrib import admin
from django.contrib.auth.models import Group

from recipes.models import (
    Recipe, Ingredient, RecipeIngredient, Tag,
    TagRecipe, Follow, Favorite, Purchase
)


admin.site.site_header = "Панель администрирования Foodgram"
admin.site.site_title = "Панель администрирования Foodgram"
admin.site.index_title = "Добро пожаловать в админку"


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    search_fields = ('user', 'recipe', )
    list_filter = ('user',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    search_fields = ('title', 'unit', )
    list_filter = ('unit', )


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInline,
        TagInline
    )
    list_display = (
        'title', 'author',
        'text_trim', 'image',
        'pub_date'
    )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('slug', 'tags', )
    empty_value_display = '-пусто-'
    list_filter = ('pub_date', 'tags')


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_name',
    )
    list_filter = ('title',)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'user'
    )
    search_fields = ('author', 'user')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe'
    )
    search_fields = ('recipe', 'user')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(RecipeIngredient)
admin.site.register(Tag, TagAdmin)
# admin.site.register(TagRecipe)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)

admin.site.unregister(Group)
