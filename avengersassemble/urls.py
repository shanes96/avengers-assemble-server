from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from avengersassembleapi.views import create_checkout_session
from rest_framework import routers
from django.urls import path
from avengersassembleapi.views import register_user, login_user, get_cart_total
from avengersassembleapi.views import AvengerUserView, UserTeamView, VoteView, CharacterView, BattleView, CharacterTeamView, ComicView,UserComicView, UserMovieView,MovieView, CartView, CartComicView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', AvengerUserView, 'user')
router.register(r'teams', UserTeamView, 'team')
router.register(r'characterteams', CharacterTeamView, 'characterteam')
router.register(r'characters', CharacterView, 'characters')
router.register(r'comics', ComicView, 'comic')
router.register(r'usercomics', UserComicView, 'usercomics')
router.register(r'usermovies', UserMovieView, 'usermovies')
router.register(r'movies', MovieView, 'movie')
router.register(r'battles', BattleView, 'battle')
router.register(r'votes', VoteView, 'vote')
router.register(r'carts', CartView, 'cart')
router.register(r'cartcomics', CartComicView, 'cartcomic')


urlpatterns = [
    path('register', register_user),
    path('get-cart-total', get_cart_total),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('create-checkout-session', create_checkout_session)
]
