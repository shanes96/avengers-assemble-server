from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import UserMovie, AvengerUser, Movie

class UserMovieView(ViewSet):
    def retrieve(self, request, pk):
        user_view = UserMovie.objects.get(pk=pk)
        serialized = UserMovieSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        user_view = UserMovie.objects.all()
        serialized = UserMovieSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = UserMovie.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        avenger_user = AvengerUser.objects.get(user=request.auth.user)
        movie_id = Movie.objects.get(pk=request.data["movie"])
        user_movie = UserMovie.objects.create(
            movie= movie_id,
            user= avenger_user
        )
        serializer = UserMovieSerializer(user_movie)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

class UserMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMovie
        fields = ('id', 'user')
        depth=2