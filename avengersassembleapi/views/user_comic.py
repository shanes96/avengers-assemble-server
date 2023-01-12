from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import UserComic, AvengerUser, Comic

class UserComicView(ViewSet):
    def retrieve(self, request, pk):
        user_view = UserComic.objects.get(pk=pk)
        serialized = UserComicSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = UserComic.objects.all()
        if "myComics" in request.query_params:
            avengerUser= AvengerUser.objects.get(user=request.auth.user)
            user_view = Comic.objects.filter(user=avengerUser)
        serialized = UserComicSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = UserComic.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        avenger_user = AvengerUser.objects.get(user=request.auth.user)
        comic_id = Comic.objects.get(pk=request.data["comic"])
        user_comic = UserComic.objects.create(
            comic= comic_id,
            user= avenger_user
        )
        serializer = UserComicSerializer(user_comic)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

class UserComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserComic
        fields = ('id', 'user')
        depth=2