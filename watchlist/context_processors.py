from .watchlist import Watchlist

# creating context processors so that watchlistcan be working on all pages
def watchlist(request):
    # to return the default data from watchlist
    return{ 'watchlist': Watchlist(request)}