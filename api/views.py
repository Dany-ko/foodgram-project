from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status, mixins, viewsets, filters, permissions
from rest_framework.response import Response

from api.serializer import IngredientSerializer
from recipes.models import (
    Ingredient, Favorite, Follow, Purchase
)


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class AddToFavorites(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data.get('id'),
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemoveFromFavorites(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        get_object_or_404(
            Favorite,
            recipe_id=pk,
            user=request.user
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class AddToFollow(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data.get('id')
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemoveFromFollow(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        get_object_or_404(
            Follow,
            user=request.user,
            author_id=pk
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class AddPurchase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        Purchase.objects.get_or_create(
            user=request.user,
            recipe_id=request.data.get('id')
        )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class RemovePurchase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        get_object_or_404(
            Purchase,
            recipe_id=pk,
            user=request.user
        ).delete()
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )
