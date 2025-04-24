from pyexpat.errors import messages

from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from .models import Past
from django.core.paginator import Paginator


# Create homepage.

def home(request):
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST["past_responses"]

        openai.api_key = "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"

        # create OpenAI instance
        openai.Model.list()
        try:
        # Make a completion
            response = openai.Completion.create(
                model = "gpt-3.5-turbo-instruct",
                prompt = question,
                temperature = 0,
                max_tokens = 60,
                top_p = 1.0,
                frequency_penalty = 0.0,
                presence_penalty = 0.0
            )
            # parse response
            response = (response["choices"][0]["text"]).strip()

            if "hoodilydaddle" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"
                #save to database
                record = Past(question = question, answer = response)
                record.save()

            return render(request, 'Home.html', {"question": question, "response": response, "past_responses": past_responses})
        except Exception as e:
            return render(request, 'Home.html', {"question": question, "response": e, "past_responses": past_responses})
    return render(request, 'Home.html', {})
def past(request):
    p = Paginator(Past.objects.all(), 5)
    page = request.GET.get('page')
    pages = p.get_page(page)
    past = Past.objects.all()

    nums = "x" * pages.paginator.num_pages


    return render(request, "past.html", {"past":past, "pages":pages, "nums":nums})

def delete_past(request, Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, "That Question and Answer have been deleted.")
