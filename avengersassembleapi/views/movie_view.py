from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Movie,AvengerUser


class MovieView(ViewSet):
    def retrieve(self, request, pk):
        comic_view = Movie.objects.get(pk=pk)
        serialized = MovieSerializer(comic_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        specific_user_movie_view = Movie.objects.all()
        if "myMovies" in request.query_params:
            avengerUser= AvengerUser.objects.get(user=request.auth.user)
            specific_user_movie_view= Movie.objects.filter(avengeruser=avengerUser)
        serialized = MovieSerializer(specific_user_movie_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Movie.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        movie = Movie.objects.create(
            movie_id=request.data['movie_id'],
            movie_title=request.data['movie_title'],
            movie_picture=request.data['movie_picture'],
        )
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id','movie_id', 'movie_title', 'movie_picture')
        depth=1