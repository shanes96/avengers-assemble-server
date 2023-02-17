from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from avengersassembleapi.views import register_user, login_user, add_subscriber_to_mailchimp
from avengersassembleapi.views import AvengerUserView, UserTeamView, VoteView, CharacterView, BattleView, CharacterTeamView, ComicView,UserComicView, UserMovieView,MovieView

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

urlpatterns = [
    path('register', register_user),
    path('email', add_subscriber_to_mailchimp),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
