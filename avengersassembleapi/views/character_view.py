from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Character


class CharacterView(ViewSet):
    def retrieve(self, request, pk):
        user_view = Character.objects.get(pk=pk)
        serialized = CharacterSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = Character.objects.all()
        serialized = CharacterSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Character.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        character = Character.objects.create(
            character_id=request.data['character_id'],
            character_name=request.data['character_name'],
            character_picture=request.data['character_picture'],
            character_extension=request.data['character_extension']
        )
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('id','character_id', 'character_name', 'character_picture','character_extension' )
        depth=1