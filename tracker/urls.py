from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserCreateView, CustomTokenObtainPairView, ActivityListCreateView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activities/', ActivityListCreateView.as_view(), name='activities'),
]
