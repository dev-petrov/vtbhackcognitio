from django.shortcuts import render
from django.http import HttpResponse, Http404


# Create your views here.

def edid_document(requset, document_id):
   # asyncio.run(async_comments(requset, doc_id)) asyncio.
    for i in range(3):
        time.sleep(1)
    #data = list(loop.run_until_complete(asyncio.wait([async_comments(requset, document_id)])))#[0].split('=')[1].strip('\'\'>')
    return HttpResponse('data')



def add_comment(request, document_id):
    pass

def add_result(request, document_id):
    pass