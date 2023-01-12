"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Vote,AvengerUser,Battle,UserTeam

class VoteView(ViewSet):
    def retrieve(self, request, pk):
        user_view = Vote.objects.get(pk=pk)
        serialized = VoteSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = Vote.objects.all()
        serialized = VoteSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = AvengerUser.objects.get(user=request.auth.user)
        battle_id = Battle.objects.get(pk=request.data["battle"])
        user_team_voted_for_id = UserTeam.objects.get(pk=request.data["user_team_voted_for"])

        # Check if the user has already voted on this battle
        vote = Vote.objects.filter(user=user, battle=battle_id).first()
        if vote:
            # If the user has already voted, check if they are trying to vote for the same team again
            if vote.user_team_voted_for == user_team_voted_for_id:
                return Response(
                {'error': 'User has already voted for this team in this battle'},
                status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                {'error': 'User has already voted on this battle'},
                status=status.HTTP_400_BAD_REQUEST
                )

        vote = Vote.objects.create(
            user=user,
            battle=battle_id,
            user_team_voted_for=user_team_voted_for_id
        )
        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk):
        user = Vote.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id','user', 'battle', 'user_team_voted_for')
        depth=2