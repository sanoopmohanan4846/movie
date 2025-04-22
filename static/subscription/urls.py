from django.urls import path
from . import views

urlpatterns = [
    path ('subscription',views.subscription, name="subscription"),
    path ('create_subscription',views.create_subscription, name="create_subscription"),
    path ('my_sub',views.my_sub, name="my_sub"),
    
    path ('cancel_subscription/<subscription_id>/',views.cancel_subscription, name="cancel_subscription"),
]