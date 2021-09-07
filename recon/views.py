from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pymongo import MongoClient
from pymongo.database import Database
from recon.utils import utils

# Create your views here.

mongo = MongoClient()
username = "username"
projectname = "projectname"

# Making Connection
myclient = MongoClient("mongodb://mongodb:27017/") 
   
# database 
db = myclient[username]
   
# Created or Switched to collection 
# names: GeeksForGeeks
Collection = db[projectname]


def subdomains(request):
    resources = Collection.find()
    if request.method == 'POST':
        response = utils.get_resources_csv_file(resources)
        return response

    return render(request, 'database_resources.html', {'object_list': resources})
