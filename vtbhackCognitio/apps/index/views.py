from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, Http404
import json
from .models import User, Document, Result, Comment
from .serializers import ResultSerializer, CommentSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    user = request.user
    if (request.user.is_authenticated):
        return redirect('/docs/')
    else:
        return redirect('/auth/')
@csrf_exempt
def login_user(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email = email, password = password)
    if (user is not None):
        login(request, user)
        res = redirect('/docs/')
        res.set_cookie('user', user.id)
        return res
    else:
        return redirect('/auth/')

@login_required(login_url='/auth/')
def docs(request):
    user = request.user
    documents = user.document_set.filter(is_active = True)
    print(documents)
    prev_documents = user.document_set.filter(is_active = False)
    return render(request, 'index/doc_list.html', {'documents':documents, 'prev_documents': prev_documents})


@login_required(login_url='/auth/')
def document(request, document_id):
    user = request.user
    try:
        document = user.document_set.get(id = document_id)
    except:
        return redirect('/permission_denied/')
    yes = 0
    no = 0
    comments = document.comment_set.all()
    results = document.result_set.all()
    for i in results:
        if (i.result == Result.YES):
            yes += 1
        elif (i.result == Result.NO):
            no += 1
    user_point = results.get(user = user) 
    results = results.exclude(user = user)
    results = ResultSerializer(results, many=True)
    comments = CommentSerializer(comments, many=True)
    return render(request, 'index/document.html', {'document': document, 'results':results.data, 'yes': yes, 'no': no, 'comments': comments.data, 'user_point' : user_point})
@login_required(login_url='/auth/')
def logout_user(request):
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