from .models import ApplicationUser, MessageHolder
import json
import requests
from django.http import JsonResponse
from datetime import datetime

TOKEN = "367274256:AAFh1eeLfF8QIqC7XH0KcoR4pIIK7o_7Y_k"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def store_data(request):
    updates = get_updates()
    i = 0
    while i < len(updates["result"]):
        if not ApplicationUser.objects.filter(user_id=updates["result"][i]["message"]["from"]["id"]).exists():
            app_user = ApplicationUser(user_id=updates["result"][i]["message"]["from"]["id"],
                                       first_name=updates["result"][i]["message"]["from"]["first_name"],
                                       username=updates["result"][i]["message"]["from"]["username"])
            app_user.save()
        print(updates["result"][i]["message"]["date"])
        print(datetime.date(updates["result"][i]["message"]["date"]))
        app_user = ApplicationUser.objects.get(user_id=updates["result"][i]["message"]["from"]["id"])
        message = MessageHolder(user_id=app_user,
                                message=updates["result"][i]["message"]["text"],
                                message_id=updates["result"][i]["message"]["message_id"])
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


def get_last_chat_id_and_text(updates):
    print(updates)
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
