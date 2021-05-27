from django.contrib import admin
# from django import forms
from recipes.models import (
    Recipe, Ingredient, RecipeIngredient, Tag,
    TagRecipe, Follow, Favorite, User, Purchase
)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


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
    list_filter = ('pub_date', 'author', 'tags')


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_name',
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'user'
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe'
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagRecipe)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
