from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from polls.models import Question, Choice
from django.template import RequestContext, loader
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list' : latest_question_list})

def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  
    return render(request, 'polls/detail.html', {'question' : question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', { 'question' : question })

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : p,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:result', args=(p.id,)))