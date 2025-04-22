
from movieapp.models import Movies


class Watchlist():
    def __init__(self, request):
        self.session = request.session
        
        # to get the current session key if it exits
        watchlist = self.session.get('session_key')
        
        # for new user, to create a session key.
        if 'session_key' not in request.session:
            watchlist = self.session['session_key'] = {}
            
        # to get the watchlist session is avaliable in all pages of the site
        self.watchlist = watchlist
        
        
    def get_prods(self):
		# Get ids from cart
        movie_ids = self.watchlist.keys()
		# Use ids to lookup products in database model
        movies = Movies.objects.filter(id__in=movie_ids)

		# Return those looked up products
        return movies
        
        
    def add(self, movies):
        movies_id = str(movies.id)
		# Logic
        if movies_id in self.watchlist:
            pass
        else:
            self.watchlist[movies_id] = {'Title': str(movies.Title)}
            
            self.session.modified = True
		
  
    def __len__(self):
        return len(self.watchlist)
    
    def delete(self, movie_id):
        movie_id = str(movie_id)  # Ensure it's a string (same as stored keys)
        
        if movie_id in self.watchlist:
            del self.watchlist[movie_id]
            self.session["watchlist"] = self.watchlist  # Update session data
            self.session.modified = True  # Ensure session is saved

		