from .models import ApplicationUser, MessageHolder
import json
import requests
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .constants import URL, exploreByKeyword, headers, exploreByUserName, exploreByDate
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

"""
@Method_Name: store_data_web_hook
@Param_in: request
@:returns: HttpResponse
@Description: This Method receives HTTPS POST requests from telegram Bot API which contains a JSON-serialized data
"""


@csrf_exempt
@require_POST
def store_data_web_hook(request):
    try:
        updates = json.loads(request.body.decode('utf-8'))
        user_name = ""
        if "username" in updates["message"]["from"]:
            user_name = updates["message"]["from"]["username"]

        if not ApplicationUser.objects.filter(user_id=updates["message"]["from"]["id"]).exists():
            app_user = ApplicationUser(user_id=updates["message"]["from"]["id"],
                                       first_name=updates["message"]["from"]["first_name"],
                                       username=user_name)
            app_user.save()

        app_user = ApplicationUser.objects.get(user_id=updates["message"]["from"]["id"])
        message = MessageHolder(user_id=app_user,
                                message=updates["message"]["text"],
                                message_id=updates["message"]["message_id"],
                                message_date=datetime.fromtimestamp(updates["message"]["date"]))
        message.save()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


"""
@Method_Name: store_data
@Param_in: request
@:returns: HttpResponse
@Description: This Method can be used as an alternate to Webhook, When this method get invoked It fetches all the 
updates from Telegram Bot
"""


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


"""
@Method_Name: search_content
@Description: This method fetches content.
"""


def get_updates():
    url = URL + "getUpdates"
    return get_data(url)


def get_data(url):
    return json.loads(get_url(url))


def get_url(url):
    response = requests.get(url)
    return response.content.decode("utf8")


"""
@Method_Name: search_content
@Param_in: request
@:returns: Page
@Description: This Method renders Search page.
"""


def index(request):
    try:
        return render(request, 'Webcrawler/index.html')
    except Exception as e:
        print(e)


"""
@Method_Name: search_content
@Param_in: request
@:returns: Json Response
@Description: This Method build requests to invoke REST APIs based on the user query type.
"""


def search_content(request):
    try:
        search_type = request.GET.get('type', "")
        search_text = request.GET.get('text', "")

        if search_type == "Keyword" and search_text != "":
            payload = {'keyword': search_text}
            return get_data(request, exploreByKeyword, headers, payload)

        elif search_type == "Username" and search_text != "":
            payload = {'username': search_text}
            return get_data(request, exploreByUserName, headers, payload)

        elif search_type == "Date" and search_text != "":
            payload = {'query_date': search_text}
            return get_data(request, exploreByDate, headers, payload)
        else:
            return render(request, 'Webcrawler/index.html', {'search_results': "No Results Found :("})

    except Exception as e:
        print(e)
        return HttpResponseRedirect(redirect_to=reverse('index'))


"""
@Method_Name: get_data
@Param_in: request,url,header,payload
@Description: This Method invokes REST APIs to fetch data based on the user query type
"""


def get_data(request, url, header, payload):
    resp = requests.post(url=url,
                         data=json.dumps(payload),
                         headers=header)
    if resp.status_code == 200:
        return render(request, 'Webcrawler/index.html', {'search_results': resp.json()})
    else:
        return render(request, 'Webcrawler/index.html', {'search_results': "No Results Found :("})
    pass
