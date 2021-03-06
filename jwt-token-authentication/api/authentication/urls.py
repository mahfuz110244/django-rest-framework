from django.conf.urls import url

from .views import (
    LoginAPIView, RegistrationAPIView, CustomUserAPIView
)

urlpatterns = [
    # url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/registration?$', RegistrationAPIView.as_view()),
    url(r'^users/login?$', LoginAPIView.as_view()),
    url(r'^users/reg/?$', CustomUserAPIView.as_view()),
]
