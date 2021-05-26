from django.urls import path, include

from recipes import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'recipe/<slug:slug>/',
        views.RecipeDetailView.as_view(),
        name='recipe_detail'
    ),
    path(
        'recipe_create/',
        views.recipe_create,
        name='recipe_create'
    ),
    path(
        'recipe/<slug:slug>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'tags_for_page/',
        views.TagDetailView.as_view(),
        name='tags_for_page'
    ),
    path(
        'tag_list/<str:display_name>/',
        views.TagListView.as_view(),
        name='tag_detail'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    path(
        'profile/<str:username>/follow/',
        views.FollowView.as_view(),
        name='follow'
    ),
    path(
        'profile/<str:username>/favorites/',
        views.FavoriteView.as_view(),
        name='favorites'
    ),
    path(
        'profile/<str:username>/shop_list/',
        views.ShopListView.as_view(),
        name='shop_list'
    ),
    path(
        'generate_pdf/',
        views.generate_pdf,
        name='generate_pdf'
    ),
    path('api/', include('api.urls')),
]
