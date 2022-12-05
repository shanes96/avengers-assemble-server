"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Battle


class BattleView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        user_view = Battle.objects.get(pk=pk)
        serialized = BattleSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        user_view = Battle.objects.all()
        serialized = BattleSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Battle.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class BattleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Battle
        fields = ('id', 'team_1', 'team_2')
        depth=1