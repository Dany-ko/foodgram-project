from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    GetIngredient, AddToFavorites,
    RemoveFromFavorites,
    AddToFollow, RemoveFromFollow,
    AddPurchase, RemovePurchase
)


router = DefaultRouter(trailing_slash=False)


router.register(
    r'ingredients',
    GetIngredient,
    basename='ingredients'
)

urlpatterns = [
    path('', include(router.urls)),
    path('favorites/',  AddToFavorites.as_view()),
    path('favorites/<int:pk>/',  RemoveFromFavorites.as_view()),
    path('follow/', AddToFollow.as_view()),
    path('unfollow/<int:pk>/', RemoveFromFollow.as_view()),
    path('purchases/', AddPurchase.as_view()),
    path('purchases/<int:pk>/', RemovePurchase.as_view()),
]
