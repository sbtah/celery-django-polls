import json
import random
import requests

from celery.result import AsyncResult
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from polls.forms import YourForm
from polls.tasks import sample_task


# Helpers
def api_call(email):
    # Used for testing a failed API Call.
    if random.choice([0, 1]):
        raise Exception("Random processing error.")

    # Simulating API Call.
    requests.post("https://httpbin.org/delay/5")


# Views
def subscribe(request):
    if request.method == "POST":
        form = YourForm(request.POST)
        if form.is_valid():
            task = sample_task.delay(form.cleaned_data["email"])
            # Return the task ID so the JS can poll the state.
            return JsonResponse(
                {
                    "task_id": task.task_id,
                }
            )
    form = YourForm()
    return render(request, "form.html", {"form": form})


def task_status(request):
    task_id = request.GET.get("task_id")

    if task_id:
        task = AsyncResult(task_id)
        state = task.state

        if state == "FAILURE":
            error = str(task.result)
            response = {
                "state": state,
                "error": error,
            }
        else:
            response = {
                "state": state,
            }
        return JsonResponse(response)


@csrf_exempt
def webhook_test(request):
    # if not random.choice([0, 1]):
    #     raise Exception()

    # blocking process
    requests.post("https://httpbin.org/delay/5")
    return HttpResponse("Pong!")
