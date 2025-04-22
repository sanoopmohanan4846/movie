from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
import uuid


# password reset for forgot password
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    reset_id = models.UUIDField(default = uuid.uuid4, unique=True, editable=False )
    
    def __str__(self):
        return f"password reset of {self.user.username} at {self.created}"


# Movie category
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Movies(models.Model):
    # Basic movie details
    Title = models.CharField(max_length=30)  # The title of the movie
    Description = models.CharField(max_length=1000, blank=True, null=True)  # A brief description or synopsis
    Rate = models.FloatField(max_length=11)  # The rating of the movie (e.g., IMDb score)
    Uuid = models.UUIDField(default=uuid.uuid4)  # Unique identifier for each movie
    File = models.FileField(upload_to='video')  # File path for the movie video
    Image = models.ImageField(upload_to='img')  # Image related to the movie (e.g., thumbnail)
    Poster = models.ImageField(upload_to='poster')  # Poster image for the movie
    genrez = models.ManyToManyField(Genre, related_name='movies')
    duration = models.DurationField(default=timedelta(hours=0, minutes=0), help_text="Duration in HH:MM format.") # The runtime of the movie
    release_date = models.DateField(default=date.today)  # The release date of the movie (used for New Releases and Upcoming)
    subscription = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Title

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username
