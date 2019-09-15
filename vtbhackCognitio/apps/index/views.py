from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, Http404
import json
from .models import User, Document, Result, Comment
from .serializers import ResultSerializer

# Create your views here.
def index(request):
    user = request.user
    if (request.user.is_authenticated):
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
    return render(request, 'index/doc_list.html', {'documents':documents})


@login_required(login_url='/auth/')
def document(request, document_id):
    user = request.user
    try:
        document = user.document_set.get(id = document_id)
    except:
        return redirect('/permission_denied/')
    results = document.result_set.all()
    yes = 0
    no = 0
    comments = document.comment_set.all()
    for i in results:
        if (results.type == Result.YES):
            yes += 1
        elif (results.type == Result.NO):
            no += 1
    results = ResultSerializer(results)
    return render(request, 'index/document.html', {'document': document, 'results':results, 'yes': yes, 'no': no, 'comments': comments})

@login_required(login_url='/auth/')
def logout(request):
    logout(request)
    return redirect('/auth/')

@login_required(login_url='/auth/')
def create_doc(request):
    user = request.user
    if (not user.is_stuff):
        return redirect('/permisson_denied/')
    else:
        return render(request, 'index/create_doc.html')

@login_required(login_url='/auth/')
def edit_doc(request, document_id):
    user = request.user
    if (not user.is_stuff):
        return redirect('/permisson_denied/')
    else:
        try:
            document = Document.objects.get(id = document_id)
        except:
            return Http404('Not found')
        return render(request, 'index/create_doc.html', {'document':document})

def auth(request):
    
    return render(request, 'index/auth.html')