from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
import json
from .models import User, Document

# Create your views here.
def index(request):
    user = request.user
    if (user.is_authenticated()):
        return redirect('/docs/')
    else:
        return redirect('/auth/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email = email, password = password)
    if (user != None):
        login(request, user)
        return HttpResponse(json.dumps({
            'type': 'success'
        }))
    else:
        return HttpResponse(json.dumps({
            'type':'invalid'
        }))

@login_required(login_url='/auth/')
def docs(request):
    user = request.user
    documents = user.document_set.all()
    return render(request, 'index/doc_list.html', ['documents':document])


@login_required(login_url='/auth/')
def document(request, document_id):
    pass

@login_required(login_url='/auth/')
def logout(request):
    pass

