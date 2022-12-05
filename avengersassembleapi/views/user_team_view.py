"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import UserTeam


class UserTeamView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        user_view = UserTeam.objects.get(pk=pk)
        serialized = UserTeamSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        user_view = UserTeam.objects.all()
        serialized = UserTeamSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = UserTeam.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class UserTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTeam
        fields = ('id', 'name', 'user')
        depth=1