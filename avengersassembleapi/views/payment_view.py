# from django.conf import settings
# from django.http import HttpResponseBadRequest, JsonResponse
# from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from avengersassembleapi.models import Cart


# import stripe

# stripe.api_key = 'secret key goes here'

# YOUR_DOMAIN = 'http://localhost:8000'

# @require_POST
# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'POST':
#         try:
#             # Get the user's cart
#             cart_id = 1 # replace with the actual cart id
#             print("Cart ID:", cart_id)
#             cart = Cart.objects.get(id=cart_id)
#             print("Cart:", cart)

#             # Create the line items for the checkout session
#             line_items = []
#             for cart_comic in cart.comics.all():
#                 line_item = {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': 1000,
#                         'product_data': {
#                             'name': cart_comic.comic_title,
#                         },
#                     },
#                     'quantity': 1
#                 }
#                 line_items.append(line_item)

#             # Create a Checkout Session
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url='http://localhost:3000/success',
#                 cancel_url='http://localhost:3000/cancel',
#             )

#             return JsonResponse({'id': session.id})

#         except Cart.DoesNotExist:
#             return JsonResponse({'error': 'Cart not found'})
