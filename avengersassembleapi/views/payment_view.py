# #! /usr/bin/env python3.6

# """
# server.py
# Stripe Sample.
# Python 3.6 or newer required.
# """
# import os
# from flask import Flask, redirect, request

# import stripe
# # This is a public sample test API key.
# # Don’t submit any personally identifiable information in requests made with this key.
# # Sign in to see your own test API key embedded in code samples.
# stripe.api_key = 'pk_test_51MgEV5GHHR2V7NucWuyGmThcvbO98QphWMno3G9MwuqLOTikqX4uk36VnziJkW1hYDe7jZBP97G44Er0qOQvxxbD00Rb7Bu2bZ'
# product = stripe.Product.create(name="Amazing Fantasy 15")

# price = stripe.Price.create(
#     product=product.id,
#     unit_amount=2000,
#     currency="usd"
# )

# app = Flask(__name__,
#             static_url_path='',
#             static_folder='public')

# YOUR_DOMAIN = 'http://localhost:3000'

# @app.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     'price': 'price_1MgX0gGHHR2V7NucxQyG7IrP',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '?success=true',
#             cancel_url=YOUR_DOMAIN + '?canceled=true',
#         )
#     except Exception as e:
#         return str(e)

#     return redirect(checkout_session.url, code=303)

# if __name__ == '__main__':
#     app.run(port=8000)