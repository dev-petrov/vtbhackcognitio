from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from index.models import User, Document, Comment
import json, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Create your views here.

def edit_document(requset, document_id):
    pass
    #return HttpResponse('data')

@csrf_exempt
@login_required(login_url = '/auth/')
def add_comment(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
    except:
        return Http404
    user = request.user
    print(datetime.datetime.now())
    comment = document.comment_set.create(user = user, text=request.POST['text'], date = datetime.datetime.now())
    comment.save()
    return HttpResponse(json.dumps({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'text': comment.text,
        'date': comment.date.strftime('%Y-%m-%d %X')
    }))
@csrf_exempt
@login_required(login_url = '/auth/')
def add_result(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
    except:
        return Http404
    user = request.user
    result = document.result_set.get(user = user, date = datetime.datetime.now())
    result.upate(result = request.POST['result'])
    return HttpResponse(json.dumps({
        'result': comment.text,
        'date': comment.date.strftime('%Y-%m-%d %X')
    }))