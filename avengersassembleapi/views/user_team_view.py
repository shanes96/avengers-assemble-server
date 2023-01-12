from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import UserTeam,AvengerUser,Character, Vote

class UserTeamView(ViewSet):
    def retrieve(self, request, pk):
        user_team = UserTeam.objects.get(pk=pk)
        votes= Vote.objects.all()
        total_team_votes=[]
        for vote in votes:
            if user_team.id == vote.user_team_voted_for.id:
                total_team_votes.append(vote)
                user_team.number_of_votes = len(total_team_votes)
        serialized = UserTeamSerializer(user_team, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        user_teams = UserTeam.objects.all()
        votes = Vote.objects.all()

        for user_team in user_teams:
            user_team_votes = []
            for vote in votes:
                if vote.user_team_voted_for.id == user_team.id:
                    user_team_votes.append(vote)
                    user_team.number_of_votes= len(user_team_votes)
                    
        if "myTeams" in request.query_params:
            avengerUser = AvengerUser.objects.get(user=request.auth.user)
            user_teams = user_teams.filter(user=avengerUser)
        serialized = UserTeamSerializer(user_teams, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = UserTeam.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        user = AvengerUser.objects.get(user=request.auth.user)
        team = UserTeam.objects.create(
            user=user,
            team_name=request.data['team_name']
        )
        serializer = UserTeamSerializer(team)
        return Response(serializer.data)

    def update(self, request, pk):
        team = UserTeam.objects.get(pk=pk)
        team.team_name = request.data["team_name"]
        team.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class AvengerUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model= AvengerUser
        fields = ('id','full_name','bio','profile_image','favorite_comics','favorite_movies',)

class CharacterInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model= Character
        fields = ('id','character_id','character_name','character_picture')


class UserTeamSerializer(serializers.ModelSerializer):
    user=AvengerUserInfoSerializer(many=False)
    characters= CharacterInfoSerializer
    class Meta:
        model = UserTeam
        fields = ('id', 'user', 'characters', 'team_name',)
        depth=3