from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Comic,AvengerUser


class ComicView(ViewSet):
    def retrieve(self, request, pk):
        comic_view = Comic.objects.get(pk=pk)
        serialized = ComicSerializer(comic_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        specific_user_comic_view = Comic.objects.all()

        if "myComics" in request.query_params:
            avengerUser= AvengerUser.objects.get(user=request.auth.user)
            specific_user_comic_view = Comic.objects.filter(avengeruser=avengerUser)
        serialized = ComicSerializer(specific_user_comic_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Comic.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        comic = Comic.objects.create(
            comic_id=request.data['comic_id'],
            comic_title=request.data['comic_title'],
            comic_picture=request.data['comic_picture'],
            comic_extension=request.data['comic_extension'],
            comic_price=request.data['comic_price'],

        )
        serializer = ComicSerializer(comic)
        return Response(serializer.data)
    
    def update(self, request, pk):
        comic = Comic.objects.get(pk=pk)
        comic.quantity=request.data["quantity"]
        comic.save()
        serializer = ComicSerializer(comic)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comic
        fields = ('id','comic_id', 'comic_title', 'comic_picture','comic_extension')
        depth=1