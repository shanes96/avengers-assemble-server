#! /usr/bin/env python3.6

import os
from flask import Flask, redirect, request, jsonify

import stripe

stripe.api_key = 'secret key goes here'
product = stripe.Product.create(name="Amazing Fantasy 15")

price = stripe.Price.create(
    product=product.id,
    unit_amount=2000,
    currency="usd"
)

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1MgX0gGHHR2V7NucxQyG7IrP',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/test-payment?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)
