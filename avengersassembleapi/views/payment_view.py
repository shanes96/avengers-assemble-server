from decimal import Decimal
from django.http import HttpResponseServerError, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from avengersassembleapi.models import Comic,AvengerUser, CartComic
from rest_framework.decorators import action
import os
from flask import Flask, redirect, request, jsonify
import mailchimp



from avengersassembleapi.models.cart import Cart

def get_cart_total(request, pk):
            cart_comics = CartComic.objects.filter(cart=pk)
            total = 0
            for cart_comic in cart_comics:
                comic_price = float(cart_comic.comic.comic_price)
                quantity = cart_comic.quantity
                total += comic_price * quantity
            return Response({'total': total})


        # create a virtual property called "total" on the cart comics model that will contain the total number 
        #  create a function that will count the quantity for each comic 
        # once the quantity is determined multiply the number to the comic price which is $10
        # once this is is calulcated do the same for the rest of the comics

class CartComicView(ViewSet):
    def retrieve(self, request, pk):
        comic_view = CartComic.objects.get(pk=pk)
        serialized = CartComicSerializer(comic_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        specific_user_comic_view = CartComic.objects.all()

        if "myComics" in request.query_params:
            avengerUser= AvengerUser.objects.get(user=request.auth.user)
            specific_user_comic_view = CartComic.objects.filter(avengeruser=avengerUser)
        serialized = CartComicSerializer(specific_user_comic_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = CartComic.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        comic = CartComic.objects.get(pk=pk)
        comic.quantity = request.data["quantity"]
        comic.save()
        serializer = CartComicSerializer(comic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import stripe
# This is your test secret API key.
stripe.api_key = 'secret key here'
tax_rate = stripe.TaxRate.create(
  display_name="Sales Tax",
  description="Sales tax for example state",
  jurisdiction="US",
  percentage=6.0,
  inclusive=False,
)
@csrf_exempt
def create_checkout_session(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart_id = cart.id
    cart_comics = CartComic.objects.filter(cart__id=cart_id)
    line_items = []
    cart_total = Decimal(0.00)
    for item in cart_comics:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "unit_amount":int(str(item.comic.comic_price).replace('.', '')),
                "product_data": {
                    "name": item.comic.comic_title,
                },
                "unit_amount":int(str(item.comic.comic_price).replace('.', '')),
            },
            "quantity": item.quantity,
            "tax_rates": [tax_rate.id],

        })
        cart_total += Decimal(item.cart_total.replace('$', ''))

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        success_url='http://localhost:3000/success',
        cancel_url='http://localhost:3000/cancel',
    )
    response = JsonResponse({"id": session.id, "cart_total": str(cart_total)})
    response['X-Frame-Options'] = 'ALLOW-FROM http://localhost:3000'
    return response


class CartComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartComic
        fields = ('id','cart', 'comic', 'quantity', 'comic_sub_total', 'cart_total', 'cart_sub_total', 'tax', 'cart_total_quantity', 'comic_sub_total_with_tax')
        depth=3