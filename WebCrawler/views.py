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


@csrf_exempt
@require_POST
def store_data_web_hook(request):
    updates = json.loads(request.body.decode('utf-8'))
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


def index(request):
    try:
        return render(request, 'Webcrawler/index.html')
    except Exception as e:
        print(e)


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


def get_data(request, url, header, payload):
    resp = requests.post(url=url,
                         data=json.dumps(payload),
                         headers=header)
    if resp.status_code == 200:
        return render(request, 'Webcrawler/index.html', {'search_results': resp.json()})
    else:
        return render(request, 'Webcrawler/index.html', {'search_results': "No Results Found :("})
    pass
