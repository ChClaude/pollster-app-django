from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

"""
Each view is responsible for doing one of two things: returning an HttpResponse object containing 
the content for the requested page, or raising an exception such as Http404. The rest is up to you.
"""

"""
Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party 
Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, 
using whatever Python libraries you want.

- All Django wants is that HttpResponse. Or an exception.
"""


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions ( not including those set to be
        published in the future).
        """

        """
        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date is 
        less than or equal to - that is, earlier than or equal to - timezone.now.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# We’re using two generic views here: ListView and DetailView.
# Respectively, those two views abstract the concepts of “display
# a list of objects” and “display a detail page for a particular type of object.”
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # The context is a dictionary mapping template variable names to Python objects.
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

"""


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        """
        The code for our vote() view does have a small problem. It first gets the selected_choice object from the database, then computes the new value of votes, and then saves it back to the database. If two users of your website try to vote at exactly the same time, this might go wrong: The same value, let’s say 42, will be retrieved for votes. Then, for both users the new value of 43 is computed and saved, but 44 would be the expected value.
        This is called a race condition. If you are interested, you can read Avoiding race conditions using F() to learn how you can solve this issue.
        """
        # https://docs.djangoproject.com/en/2.2/ref/models/expressions/#avoiding-race-conditions-using-f

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the back button
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
