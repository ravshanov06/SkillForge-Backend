from django.urls import path
from .views.auth import UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.posts import PostCreateView, PostListView, PostDetailView, CommmentCreateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments', CommmentCreateView.as_view(), name='comment')
]