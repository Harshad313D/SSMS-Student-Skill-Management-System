from django.urls import path
from .views import *

urlpatterns = [
    path("", custom_login, name="login"),
    path('forgot_password', forgot_pass, name='forgot_password'),
    path('confirm_otp/', confirm_otp, name='confirm_otp'),
    path('change_success', change_success, name='change_success'),
    path('logout/', logout_view, name='logout_view'),
]
