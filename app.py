# #! /usr/bin/env python3.6

# """
# server.py
# Stripe Sample.
# Python 3.6 or newer required.
# """
# import os
# from flask import Flask, redirect, request

# import stripe

# from avengersassembleapi.models.cart_comic import CartComic
# # This is your test secret API key.
# stripe.api_key = 'sk_test_51MgEV5GHHR2V7NucT5N8I9SXuwh2qWpD24dDuakwKi6RCP8lZyQ0W9c0SmR98bFPviWc8k8lX83yLpNcFSxoJUIX00lkHDH4U7'

# app = Flask(__name__,
#             static_url_path='',
#             static_folder='public')

# YOUR_DOMAIN = 'http://localhost:4242'


# @app.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session(request):
#     # Get the cart total from the request
#     cart_total = request.form['cart_total']

#     # Get the current user's cart
#     cart = CartComic.objects.get(user=request.user)

#     # Get the total quantity of items in the cart
#     cart_total_quantity = cart.cart_total_quantity

#     try:
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     # Replace with the price and currency of your product
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': cart_total,
#                         'product_data': {
#                             'name': 'Comics',
#                         },
#                     },
#                     'quantity': cart_total_quantity,
#                 },
#             ],
#             mode='payment',
#             success_url='http://localhost:3000/success',
#             cancel_url='http://localhost:3000/cancel',
#         )
#     except Exception as e:
#         return str(e)

#     return redirect(checkout_session.url)


# if __name__ == '__main__':
#     app.run(port=4242)
