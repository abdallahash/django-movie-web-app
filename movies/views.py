from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

# Create your views here.


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))


def home_page(request):
    print(str(request.GET.get('search','')))
    user_search = str(request.GET.get('search',''))
    search_result = AT.get_all(formula = "FIND('" + user_search.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method=="POST":
        data = {
            'Name' : request.POST.get('name'),
            'Pictures' : [{'url' : request.POST.get('url') or "https://api.ballotpedia.org/v3/thumbnail/"}],
            'Rating' : int(request.POST.get('rating')),
            'Notes' : request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            messages.success(request, "New movie added: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Error while creating a movie: {}".format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method =="POST":
        data = {
            'Name' : request.POST.get('name'),
            'Pictures' : [{'url':request.POST.get('url') or "https://api.ballotpedia.org/v3/thumbnail/"}],
            'Rating' : int(request.POST.get('rating')),
            'Notes' : request.POST.get('rating')
        }
        try:
            response = AT.update(movie_id, data)
            messages.success(request,"Movie updated: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Error while editing movie: {}".format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        response = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request,"Movie Deleted: {}".format(response))
    except Exception as e:
        messages.warning(request, "Error while deleting movie: {}".format(e))

    return redirect('/')

