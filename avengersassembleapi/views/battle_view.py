from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Battle,UserTeam,Vote,AvengerUser

class BattleView(ViewSet):
    def retrieve(self, request, pk):
        user_view = Battle.objects.get(pk=pk)
        serialized = BattleSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        battles = Battle.objects.all()
        teams=UserTeam.objects.all()
        for battle in battles:
            if battle.id is not None:  # only update fields for existing battles
                team_1_votes = Vote.objects.filter(user_team_voted_for=battle.team_1, battle=battle)
                battle.number_of_votes_team_1 = team_1_votes.count()
                battle.save()
        for battle in battles:
            if battle.id is not None:  # only update fields for existing battles
                team_2_votes = Vote.objects.filter(user_team_voted_for=battle.team_2, battle=battle)
                battle.number_of_votes_team_2 = team_2_votes.count()
                battle.save()
        for battle in battles:
            if battle.number_of_votes_team_1 == 2:
                battle.winner = battle.team_1
                battle.loser = battle.team_2
                print(f"Winner: {battle.winner}")
                print(f"Loser: {battle.loser}")
                battle.save()
            elif battle.number_of_votes_team_2 == 2:
                battle.winner = battle.team_2
                battle.loser = battle.team_1
                print(f"Winner: {battle.winner}")
                print(f"Loser: {battle.loser}")
                battle.save()

        if "myBattles" in request.query_params:
            user = request.auth.user
            # Get the AvengerUser object for the authenticated user
            avenger_user = AvengerUser.objects.get(user=user)
            # Filter the Battle objects to only include battles where the authenticated user is in either team_1 or team_2
            battles = Battle.objects.filter(
            (Q(team_1__user=avenger_user) | Q(team_2__user=avenger_user)) & Q(winner__isnull=True))
        serialized = BattleSerializer(battles, many=True)

        if "myCompletedBattles" in request.query_params:
            user = request.auth.user
            # Get the AvengerUser object for the authenticated user
            avenger_user = AvengerUser.objects.get(user=user)
            # Filter the Battle objects to only include battles where the authenticated user is in either team_1 or team_2
            # and where the winner is not NULL
            battles = Battle.objects.filter(
                (Q(team_1__user=avenger_user) | Q(team_2__user=avenger_user)) & ~Q(winner__isnull=True)
            )
            serialized = BattleSerializer(battles, many=True)

        if "allCurrentBattles" in request.query_params:
            battles = Battle.objects.filter(winner__isnull=True)
            serialized = BattleSerializer(battles, many=True)
            battles = serialized.data

        if "allCompletedBattles" in request.query_params:
            battles = Battle.objects.filter(winner__isnull=False)
            serialized = BattleSerializer(battles, many=True)
            battles = serialized.data
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Battle.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        team_1_id = UserTeam.objects.get(pk=request.data["team_1"])
        user_being_challenged_id = AvengerUser.objects.get(pk=request.data["user_being_challenged"])
        battle = Battle.objects.create(
            team_1=team_1_id,
            user_being_challenged=user_being_challenged_id
        )
        serializer = BattleSerializer(battle)
        return Response(serializer.data)

    def update(self, request, pk):
        battle = Battle.objects.get(pk=pk)
        team_2_id = UserTeam.objects.get(pk=request.data["team_2"])
        battle.team_2 = team_2_id
        battle.save()
        serializer = BattleSerializer(battle)
        return Response(serializer.data)

class BattleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Battle
        fields = ('id', 'team_1', 'team_2','number_of_votes_team_1', 'number_of_votes_team_2', 'winner','user_being_challenged','loser')
        depth = 2