from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from avengersassembleapi.models import AvengerUser,Comic

class AvengerUserView(ViewSet):
    def retrieve(self, request, pk):
        user_view = AvengerUser.objects.get(pk=pk)
        serialized = AvengerUserSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = AvengerUser.objects.all()
            
        if "myProfile" in request.query_params:
            # avengerUser= AvengerUser.objects.get(user=request.auth.user)
            user_view = AvengerUser.objects.filter(user=request.auth.user)

        if "myComics" in request.query_params:
            avengerUser= AvengerUser.objects.get(user=request.auth.user)
            user_view = Comic.objects.filter(user=avengerUser)

        if "myOpponents" in request.query_params:
            avengerUser = AvengerUser.objects.get(user=request.auth.user)
            user_view = AvengerUser.objects.exclude(pk=avengerUser.pk)
        serialized = AvengerUserSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = AvengerUser.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        user = AvengerUser.objects.get(pk=pk)
        user.user_wins=(request.data["user_wins"])
        user.user_losses=(request.data["user_losses"])
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class AvengerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvengerUser
        fields = ('id', 'full_name', 'profile_image', 'favorite_comics', 'favorite_movies', 'user', 'user_wins', 'user_losses')
        depth=2