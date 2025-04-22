from django.urls import path
from . import views

urlpatterns = [
    path ('',views.index, name="index"),
    path('about', views.about, name="about"),
    path('genre', views.genre, name='genre'),
    path('contact', views.contact, name="contact"),
    
    path('movie/<int:movie_id>/play/', views.moviesplayer, name='moviesplayer'),
    path('moviesdetails/<int:pk>', views.moviesdetails, name="moviesdetails"),
    path ('category/<int:genre_id>/',views.category, name="category"),
    path('collection', views.collection, name='collection'),
    path('popular_movies', views.popular_movies, name="popular_movies"),
    
    path('search', views.search, name="search"),
    
    # login/register
    path('profile', views.profile_view, name='profile'),
    path('login', views.loginview, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutview, name="logout"),
    path('forgot-password', views.forgotpassword, name="forgot-password"),
    path('password-reset-send/<str:reset_id>/', views.passwordresetsend, name="password-reset-send"),
    path('reset-password/<str:reset_id>/', views.resetpassword, name="reset-password"),
]