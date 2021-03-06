from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import FileResponse
from django.views.generic.base import TemplateView

import io
import pdfkit

from foodgram_project.settings import (
    RECIPES_NUMBERS_PER_PAGE as NUM
)
from recipes.forms import RecipeForm
from recipes.models import (
    Recipe, Tag, User,
    Follow, RecipeIngredient,
    Ingredient, Purchase
)


class AboutPage(TemplateView):
    template_name = 'stat/about.html'


class TechPage(TemplateView):
    template_name = 'stat/technology.html'


def generate_pdf(request):
    recipe_author = get_object_or_404(
        User, username=request.user
    )
    purchases = recipe_author.purchases.all()
    objs = {}
    for recipe in purchases:
        for ing in recipe.recipe.recipe_ingredients.all():
            if ing.ingredient in objs.keys():
                objs[ing.ingredient] += ing.count
            else:
                objs[ing.ingredient] = ing.count
    rendered = render_to_string(
        'recipes/pdf_file.html', {'objs': objs}
    )
    pdf = pdfkit.from_string(rendered, False)
    buffer = io.BytesIO(pdf)
    return FileResponse(
        buffer, as_attachment=True, filename='ingredients.pdf'
    )


class IsFavoriteMixin:

    def get_queryset(self):
        qureyset = super().get_queryset()
        qureyset = (
            qureyset
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
        )
        return qureyset


class BaseRecipeListView(ListView, IsFavoriteMixin):
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = NUM
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.page_title

    def get_queryset(self):
        qs = super().get_queryset()
        tags = self.request.GET.getlist("tag")
        if tags:
            qs = qs.filter(tags__display_name__in=tags).distinct()
        return qs


class IndexView(BaseRecipeListView):
    page_title = '??????????????'
    template_name = 'recipes/index.html'
    extra_context = {
        'tags': Tag.objects.all()
    }

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.with_is_favorite(user_id=user.id)
        return qs


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = '??????????????????'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(
            favorites__user=self.request.user
        ).with_is_favorite(user_id=user.id)
        return qs


class RecipeDetailView(DetailView, IsFavoriteMixin):
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset
            .prefetch_related('recipe_ingredients__ingredient')
            .with_is_favorite(user_id=self.request.user.id)
        )
        return queryset


class TagDetailView(DetailView):
    queryset = Tag.objects.all()
    page_title = '????????'
    template_name = 'recipes/includes/tags_for_page.html'


class ProfileListView(BaseRecipeListView, LoginRequiredMixin):
    template_name = 'recipes/profile.html'
    extra_context = None
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        author = get_object_or_404(
            User, username=self.user
        )
        kwargs.update({
            'extra_context': {
                'tags': Tag.objects.all(),
                'following': author.following.filter(
                    user=self.request.user.id
                )
            },
        })
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User, username=kwargs.get('username')
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            author=self.user
        ).with_is_favorite(
            user_id=self.request.user.id
        )
        return qs

    def _get_page_title(self):
        return self.user.get_full_name()


class FollowView(LoginRequiredMixin, ListView):
    page_title = '?????? ????????????????'
    template_name = 'recipes/follow.html'
    context_object_name = 'follow'
    extra_context = {'recipe': Recipe.objects.all()}
    paginate_by = NUM

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User, username=kwargs.get('username')
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Follow.objects.all()
        qs = qs.filter(user=self.request.user)
        return qs


class ShopListView(LoginRequiredMixin, BaseRecipeListView):
    page_title = '???????????? ??????????????'
    template_name = 'recipes/shop_list.html'
    context_object_name = 'purchases'
    paginate_by = None

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User, username=kwargs.get('username')
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Purchase.objects.all()
        qs = qs.filter(
            user=self.request.user
        )
        return qs


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]
    return ingredients


@login_required
def recipe_create(request):
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not form.is_valid():
        context = {
            'form': form,
            'is_new': True,
        }
        return render(
            request,
            'recipes/recipe_create.html',
            context
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = []
    ingredients = get_ingredients(request)
    if ingredients:
        for title, count in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            objs.append(RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                count=count
            ))
    else:
        context = {
            'form': form,
            'error': 'error',
        }
        return render(
            request,
            'recipes/recipe_create.html',
            context
        )
    recipe.save()
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect('index')


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(
        Recipe, slug=slug
    )
    if request.user.username != recipe.author.username:
        return redirect(
            'recipe_detail',
            slug=slug
        )
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if not form.is_valid():
        context = {
            'form': form, 'recipe': recipe,
            'recipe_edit': 'recipe_edit'
        }
        return render(
            request,
            'recipes/recipe_create.html',
            context,
        )
    recipe = form.save(commit=False)
    RecipeIngredient.objects.filter(
        recipe=recipe
    ).delete()
    objs = []
    ingredients = get_ingredients(request)
    if ingredients:
        for title, count in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            objs.append(RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                count=count
            ))
    else:
        context = {
            'form': form,
            'error': 'error',
        }
        return render(
            request,
            'recipes/recipe_create.html',
            context
        )
    recipe.save()
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect(
        'recipe_detail',
        slug=recipe.slug
    )


def page_not_found(request, exception):
    return render(
        request, 'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request, 'misc/500.html',
        status=500
    )
