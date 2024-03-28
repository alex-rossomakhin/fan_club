from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, GetTokenView, SignUpView,
                    TitleViewSet, UsersViewSet, ReviewViewSet, CommentViewSet)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path('v1/auth/token/', GetTokenView.as_view(), name='token_verify'),
]
