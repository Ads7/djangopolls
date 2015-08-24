from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import views
from .models import Choice, Question
from .serializer import ChoiceSerializer,QuestionSerializer
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

class ChoicesView(APIView):
    def get(self, request,question_id,format=None):
        q=Question.get_by_id(int(question_id))
        serializer = ChoiceSerializer(q.choices, many=True)
        return Response(serializer.data)

    def post(self, request,question_id,format=None):
        serializer = ChoiceSerializer(data=request.data)
        question= Question.get_by_id(int(question_id))
        if serializer.is_valid():
            choice_list = [i for i in question.choices]
            choice_list.append(Choice(choice_text=str(request.data.get("choice_text"))))
            question.choices=choice_list
            question.put()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)



class VotesView(APIView):
    def get(self, request,question_id,choice_text,format=None):
        q=Question.get_by_id(int(question_id))
        votes=None
        votes=[i.votes for i in q.choices if i.choice_text == choice_text]
        return Response(votes)

    def post(self, request,question_id,choice_text,format=None):
        q=Question.get_by_id(int(question_id))
        for i in q.choices:
            if i.choice_text == choice_text:
                i.votes+=1
        q.put()
        return Response(status.HTTP_200_OK)

    def delete(self, request,question_id,choice_text,format=None):
        q=Question.get_by_id(int(question_id))
        for i in q.choices:
            if i.choice_text == choice_text:
                if i.votes>0:
                    i.votes-=1
        q.put()
        return Response(status.HTTP_200_OK)



class QuestionView(APIView):
    def get(self, request, format=None):
        serializer = QuestionSerializer(Question.query(), many=True)
        serializer.data
        return Response(serializer.data)

    def post(self, request,format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            q=serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    def get(self, request,question_id, format=None):
        serializer = QuestionSerializer(Question.get_by_id(int(question_id)))
        return Response(serializer.data)

    def delete(self, request,question_id,format=None):
        question_key=ndb.Key(Question,int(question_id))
        q=question_key.get()
        if q!=None:
            fut_q=q.key.delete_async()
            fut_index=index.delete_async(question_id)
            fut_index.get_result()
            fut_q.get_result()
            return Response(status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        if (Question.get_by_id(int(question_id)) !=None) and 'file' in request.data:
            q=Question.get_by_id(int(question_id))
            data = request.data["file"]
            filename = "/bucket/" + question_id
            filename = filename.replace(" ", "_")
            gcs_file = gcs.open(filename, 'w', content_type = 'image/jpeg')
            gcs_file.write(data.read())
            gcs_file.close()
            blobstore_filename = '/gs' + filename
            blob_key = blobstore.create_gs_key(blobstore_filename)
            q.image=blob_key
            q.put()
            return Response(images.get_serving_url(blob_key))
        return Response("Error")

    def get(self, request, question_id,format=None):
        if Question.get_by_id(int(question_id)) !=None:
            q=Question.get_by_id(int(question_id))
            if q.image != None:
                url=images.get_serving_url(q.image)
            url ="Empty"
            return Response(url)
        return Response("Error")

    def delete(self, request, question_id,format=None):
        if Question.get_by_id(int(question_id)) !=None:
            q=Question.get_by_id(int(question_id))
            filename="/bucket/" + question_id
            blob_key = q.image
            q.image=None
            q.put()
            if blob_key != None:
                fut_blobstore=blobstore.delete_async(blob_key)
                fut_gcs=gcs.delte_async(filename)
                fut_blobstore.get_result()
                fut_gcs.get_result()
            return Response("deleted")
        return Response("Error")



