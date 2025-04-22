from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from datetime import date
# contact page
from django.core.mail import send_mail
# auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
# new movies
from django.utils.timezone import now
from datetime import timedelta




# home 
def index(request):
    movies = Movies.objects.all()
    one_year_ago = now() - timedelta(days=200)  # Calculate one year ago
    recent_movies = Movies.objects.filter(release_date__gte=one_year_ago).order_by("-release_date")
    popular_movies = Movies.objects.all().order_by("-Rate")
    context = {
        'recent_movies': recent_movies,
        'movies':movies,
        'popular_movies': popular_movies,
    }
    
    
    return render(request, 'index.html', context)

# about us
def about(request):
    return render(request, 'about.html')

def genre(request):
    movies = Movies.objects.all()
    one_year_ago = now() - timedelta(days=200)  # Calculate one year ago
    recent_movies = Movies.objects.filter(release_date__gte=one_year_ago).order_by("-release_date")
    popular_movies = Movies.objects.all().order_by("-Rate")
    context = {
        'recent_movies': recent_movies,
        'movies':movies,
        'popular_movies': popular_movies,
    }
    return render(request, 'genre.html',context)

# contact 
def contact(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Emailz = request.POST['Emailz']
        Message = request.POST['Message']
        
        # send Email
        send_mail(
            'Message from ' + Name, # the subject of the email
            Message, # email's message
            Emailz , # the sender/users email id
            ['demomail1500@gmail.com'],  # ['2nd@gmail.com'], .... ( this the reciver's email you can add more if you want )
        )
        
        context = {
            'Name': Name,
            'Emailz':Emailz,
            'Message':Message,
            }
        return render(request, 'contact.html', context)
    else:
        return render(request, 'contact.html', )

# category page
def collection(request):
    return render(request, 'collection.html',{})

# category move details page
def category(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)  # Fetch the genre or return 404
    movies = Movies.objects.filter(genre=genre)  # Get movies belonging to the selected genre
    return render(request, 'category.html', {'movies': movies, 'genre': genre})

# movie details
def moviesdetails(request, pk):
    
    moviesdetails = Movies.objects.get(id=pk)
    popular_movies = Movies.objects.all().order_by("-Rate")
    return render(request, 'moviesdetails.html',{'moviesdetails':moviesdetails, 'popular_movies':popular_movies},)

# video player view
def moviesplayer(request, movie_id):
    moviesdetails = get_object_or_404(Movies, id=movie_id)
    return render(request, 'moviesplayer.html', {'moviesdetails': moviesdetails})



# popular movies
def popular_movies(request,):
    popular_movies = Movies.objects.all().order_by("-Rate")
    context = {
    'popular_movies': popular_movies,
        }

    return render(request, 'popularmovies.html', context)

# popular movies
def search(request):
    if request.method == "POST":
        search = request.POST['search'] # search is from input box name="search"
        search = Movies.objects.filter(Title__icontains=search)
        return render(request, 'search.html', {'search':search} )
    else:
        return render(request, 'search.html', )

    
    

    
#//////////////////////////////////////////////////   AUTHENTICATION AND REGISTER/LOGIN   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'auth/profile.html', context)


def loginview(request):
    if request.method == 'POST':
        
        # getting user inputs from frontend
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # authenticate credentials
        user = authenticate(request = request, username = username, password = password)
        if user is None:
            messages.error(request, "invalid username or password")
            return redirect('login')
        else:
            login(request, user)
            return redirect('index')
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')  # first_name inside the "request.POST.get(first_name)" is the name give in the register.html page
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_data_has_error = False
        
        # make sure username are not being used
        if User.objects.filter(username = username).exists():
            user_data_has_error = True
            messages.error(request, 'A person with this Username already exists')
        
        # make sure email  are not being used  
        if User.objects.filter(email = email).exists():
            user_data_has_error = True
            messages.error(request, "A person with this Email already exists")
            
        # validate password length : make aure password is at least 5 characters long
        if len(password)<5:
            user_data_has_error = True
            messages.error(request, "the password must have atlest 5 characters")
            
        # if the above 3 conditions are TRUE
        if user_data_has_error:
            return redirect('auth/register')
        # if there is no errors 
        else:
            new_user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password,
                ) 
            messages.success(request, "Your Accout has been created, login now")
            return redirect('login')
        
    return render(request, 'auth/register.html')

# logout
def logoutview(request):
    logout(request)
    messages.success(request, ("you are logged out. we miss you"))
    return redirect('index')

def forgotpassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-send', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'auth/forgot_password.html')


# message showing the password-reset request sending to corresponding g-mail
def passwordresetsend(request, reset_id):
    if PasswordReset.objects.filter(reset_id = reset_id).exists():    
        return render (request, 'auth/password_reset_sent.html')
    # if reset id code does'nt exist 
    else:
        messages.error(request, " invalid reset id")
        return redirect('forgot-password')
    

# password reset
def resetpassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'auth/reset_password.html')


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////