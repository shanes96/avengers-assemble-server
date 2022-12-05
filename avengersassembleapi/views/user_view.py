"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import AvengerUser


class AvengerUserView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        user_view = AvengerUser.objects.get(pk=pk)
        serialized = AvengerUserSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        user_view = AvengerUser.objects.all()
        serialized = AvengerUserSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = AvengerUser.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class AvengerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvengerUser
        fields = ('id', 'full_name', 'profile_image', 'favorite_comics', 'favorite_movies', 'user')
        depth=1

        # make views for the rest of the models
        # find out if i need to make team a "through" field on the character model