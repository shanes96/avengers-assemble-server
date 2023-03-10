from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Comic,AvengerUser, Cart, CartComic


class CartView(ViewSet):
    def retrieve(self, request, pk):
        cart_view = Cart.objects.get(pk=pk)
        serialized = CartSerializer(cart_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        carts = Cart.objects.all()
    
        if "myCart" in request.query_params:
            user = request.auth.user
            # Get the AvengerUser object for the authenticated user
            avenger_user = AvengerUser.objects.get(user=user)
            # Filter the Battle objects to only include battles where the authenticated user is in either team_1 or team_2
            carts = Cart.objects.filter(
            (Q(user=avenger_user)))
        serialized = CartSerializer(carts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = Comic.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

def create(self, request):
    avenger_user = AvengerUser.objects.get(user=request.auth.user)
    comic_id = Comic.objects.get(pk=request.data["comic"])
    try:
        cart = Cart.objects.get(user=avenger_user)
        # check if the comic is already in the cart
        if CartComic.objects.filter(cart=cart, comic=comic_id).exists():
            return Response({"message": "Comic is already in the cart"})
        else:
            # add the comic to the existing cart
            item = CartComic.objects.create(cart=cart, comic=comic_id)
            serializer = CartSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Cart.DoesNotExist:
        # create a new cart if one doesn't exist
        cart = Cart.objects.create(user=avenger_user)
        item = CartComic.objects.create(cart=cart, comic=comic_id)
        
        serializer = CartSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id','user', 'comics')
        depth=2