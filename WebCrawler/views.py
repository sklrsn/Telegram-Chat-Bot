from .models import ApplicationUser, MessageHolder
import json
import requests
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

TOKEN = "367274256:AAFh1eeLfF8QIqC7XH0KcoR4pIIK7o_7Y_k"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


@csrf_exempt
@require_POST
def store_data_web_hook(request):
    print(request.body)
    updates = json.loads(request.body)
    if not ApplicationUser.objects.filter(user_id=updates["message"]["from"]["id"]).exists():
        app_user = ApplicationUser(user_id=updates["message"]["from"]["id"],
                                   first_name=updates["message"]["from"]["first_name"],
                                   username=updates["message"]["from"]["username"])
        app_user.save()

    app_user = ApplicationUser.objects.get(user_id=updates["message"]["from"]["id"])
    message = MessageHolder(user_id=app_user,
                            message=updates["message"]["text"],
                            message_id=updates["message"]["message_id"],
                            message_date=datetime.fromtimestamp(updates["message"]["date"]))
    message.save()
    return HttpResponse(status=200)


def store_data(request):
    updates = get_updates()
    i = 0
    while i < len(updates["result"]):
        if not ApplicationUser.objects.filter(user_id=updates["result"][i]["message"]["from"]["id"]).exists():
            app_user = ApplicationUser(user_id=updates["result"][i]["message"]["from"]["id"],
                                       first_name=updates["result"][i]["message"]["from"]["first_name"],
                                       username=updates["result"][i]["message"]["from"]["username"])
            app_user.save()

        app_user = ApplicationUser.objects.get(user_id=updates["result"][i]["message"]["from"]["id"])
        message = MessageHolder(user_id=app_user,
                                message=updates["result"][i]["message"]["text"],
                                message_id=updates["result"][i]["message"]["message_id"],
                                message_date=datetime.fromtimestamp(updates["result"][i]["message"]["date"]))
        message.save()
        i = i + 1
    return JsonResponse({"Success": True})


def get_updates():
    url = URL + "getUpdates"
    return get_data(url)


def get_data(url):
    return json.loads(get_url(url))


def get_url(url):
    response = requests.get(url)
    return response.content.decode("utf8")
