from django.shortcuts import render
from django.http import HttpResponse, Http404
import asyncio, time


# Create your views here.

async def async_comments(requset, doc_id):
    await asyncio.sleep(5)
    return 'no'

def get_comments(requset, document_id):
   # asyncio.run(async_comments(requset, doc_id)) asyncio.
    for i in range(3):
        time.sleep(1)
    #data = list(loop.run_until_complete(asyncio.wait([async_comments(requset, document_id)])))#[0].split('=')[1].strip('\'\'>')
    return HttpResponse('data')



