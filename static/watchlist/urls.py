from django.urls import path
from . import views

urlpatterns = [
    path('', views.watchlist_summery , name= "watchlist_summery" ),
    path('add', views.watchlist_add , name= "watchlist_add" ),
    path('delete', views.watchlist_delete , name= "watchlist_delete" ),
]