from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import views
from .models import Choice, Question
from .serializer import QuestionSerializer
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from rest_framework import generics
from django.utils import timezone
import logging
import cloudstorage as gcs
from google.appengine.api import blobstore
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import search

index = search.Index(name='question')

logger = logging.getLogger(__name__)
# Retry can help overcome transient urlfetch or GCS issues, such as timeouts.
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)

class QuestionView(APIView):
    def get(self, request, format=None):
        #question = Question.query(id==request.GET['id']).fetch(1).to_dict()
        serializer = QuestionSerializer(Question.query(), many=True)
        serializer.data
        return Response(serializer.data)

    def post(self, request,format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

class SearchView(APIView):
    def get(self, request,format=None):
        query=request.GET.get('query')
        logger.info(query)
        try:
            search_results = index.search(query.strip())
            result=[]
            for doc in search_results:
                doc_id = doc.doc_id
                fields = doc.fields
            logger.info(search_results)
            return Response("Success")
        except search.Error:
            logger("search failed")
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    def post(self, request, question_id,format=None):
        if(Question.query(id=question_id).exists()):
            q=Question.query(id==question_id)
            data = request.data['file']
            filename = "/bucket/" + question_id
            filename = filename.replace(" ", "_")
            gcs_file = gcs.open(filename, 'w', content_type = 'image/jpeg')
            gcs_file.write(data.read())
            gcs_file.close()
            blobstore_filename = '/gs' + filename
            blob_key = blobstore.create_gs_key(blobstore_filename)
            q.image=images.get_serving_url(blob_key)
            q.save()
            return Response(images.get_serving_url(blob_key))
        return Response("Error")

