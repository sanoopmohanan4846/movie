import json
from django.shortcuts import render, get_object_or_404
from .watchlist import Watchlist
from movieapp.models import Movies
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.



def watchlist_summery(request):
    watchlist = Watchlist(request)
    watchlist_movies = watchlist.get_prods
    return render(request, "watchlist/watchlist_summery.html", {"watchlist_movies":watchlist_movies})
    
    
def watchlist_add(request):
    # Get the cart
	watchlist = Watchlist(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		moviesdetails_id = int(request.POST.get('moviesdetails_id'))
  
		# lookup product in DB
		movies = get_object_or_404(Movies, id=moviesdetails_id)
		
		# Save to session
		watchlist.add(movies=movies)
  
        # Get Cart Quantity
		watchlist_quantity = watchlist.__len__()


		

		# Return resonse
		response = JsonResponse({'qty': watchlist_quantity})
		
		return response




def watchlist_delete(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON
            movie_id = data.get("moviesdetails_id")

            if movie_id:
                watchlist = Watchlist(request)
                watchlist.delete(movie_id)

                # Check if it was deleted
                if movie_id not in watchlist.watchlist:
                    return JsonResponse({"success": True, "movies": movie_id})
                else:
                    return JsonResponse({"success": False, "error": "Movie not removed from session"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"})

    return JsonResponse({"success": False, "error": "Invalid request method"})