from rest_framework.views import APIView
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from api.serializer import IngredientSerializer
from recipes.models import (
    Ingredient, Favorite, Follow, Purchase
)


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset


class AddToFavorites(APIView):

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemoveFromFavorites(APIView):

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(
            recipe_id=pk,
            user=request.user
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class AddToFollow(APIView):

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemoveFromFollow(APIView):

    def delete(self, request, pk, format=None):
        Follow.objects.filter(
            user=request.user,
            author_id=pk
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class AddPurchase(APIView):

    def post(self, request, format=None):
        Purchase.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemovePurchase(APIView):

    def delete(self, request, pk, format=None):
        Purchase.objects.filter(
            recipe_id=pk,
            user=request.user
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )
