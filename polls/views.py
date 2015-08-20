from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import views
from .models import Choice, Question
from .serializer import ChoiceSerializer,QuestionSerializer
from django.core.urlresolvers import reverse
from django.views import generic
from rest_framework import generics
from django.utils import timezone
import cloudstorage as gcs
from google.appengine.api import blobstore
from google.appengine.api import images
from google.appengine.ext import ndb


from google.appengine.api import app_identity

# Retry can help overcome transient urlfetch or GCS issues, such as timeouts.
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)

class IndexView(generic.ListView):
    """docstring for IndexView"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """ return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'    

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

class QuestionsList(generics.ListCreateAPIView):
    queryset = Question.query()
    serializer_class = QuestionSerializer

class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Choice.query(Choice.question == question_id)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    # def put(self, request, filename, format=None):
    #     file_obj = request.FILES['file']
    #     # ...
    #     # do some staff with uploaded file
    #     # ...
    #     return Response(file_obj)
    def post(self, request, question_id,format=None):
        if(Question.query(id=question_id).exists()):
            q=Question.query(id==question_id)
            data =   request.data['file']
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

