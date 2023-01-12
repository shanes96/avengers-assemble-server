from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import CharacterTeam,Character,UserTeam

class CharacterTeamView(ViewSet):
    def retrieve(self, request, pk):
        user_view = CharacterTeam.objects.get(pk=pk)
        serialized = CharacterTeamSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = CharacterTeam.objects.all()
        serialized = CharacterTeamSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = CharacterTeam.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        character = Character.objects.get(pk=request.data["character"])
        team = UserTeam.objects.get(pk=request.data["team"])
        character_team = CharacterTeam.objects.get(pk=pk)
        character_team.team=team
        character_team.character=character
        character_team.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        character_id = Character.objects.get(pk=request.data["character"])
        team_id = UserTeam.objects.get(pk=request.data["team"])
        character_team = CharacterTeam.objects.create(
            character= character_id,
            team= team_id
        )
        serializer = CharacterTeamSerializer(character_team)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

class CharacterTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterTeam
        fields = ('id', 'team')
        depth=2