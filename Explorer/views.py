from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserNameSerializer, DateSerializer, KeyWordSerializer
from WebCrawler.models import ApplicationUser, MessageHolder
from datetime import datetime
import itertools

"""
This class  (POST method) facilitates to retrieve Messages sent by a specific user.
@Class_Name: ExploreByUsername
@Params: username
"""


class ExploreByUsername(APIView):
    @staticmethod
    def post(request):
        try:
            serializer = UserNameSerializer(data=request.data)
            if serializer.is_valid() and serializer.data['username'] != "":
                app_user = ApplicationUser.objects.get(username=serializer.data['username'])
                messages = MessageHolder.objects.filter(user_id=app_user)
                result = dict()
                data = []
                for msg in messages:
                    data.append(msg.message)
                result["messages"] = data
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(exception="Bad Request", status=status.HTTP_400_BAD_REQUEST)


"""
This class  (POST method) facilitates to retrieve Messages based on the date.
@Class_Name: ExploreByDate
@Params: query_date
"""


class ExploreByDate(APIView):
    @staticmethod
    def post(request):
        try:
            serializer = DateSerializer(data=request.data)
            if serializer.is_valid() and serializer.data['query_date'] != "":
                query_date = datetime.strptime(serializer.data['query_date'],
                                               "%Y/%m/%d")
                messages = MessageHolder.objects.filter(message_date__year=query_date.year,
                                                        message_date__month=query_date.month,
                                                        message_date__day=query_date.day)
                data = itertools.groupby(messages, lambda record: record.user_id)
                messages_by_user = [(user, list(message_this_day)) for user, message_this_day in data]
                result = dict()
                for data in messages_by_user:
                    temp = []
                    for msg in data[1]:
                        temp.append(msg.message)
                    result[str(data[0].username)] = temp
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(exception="Bad Request", status=status.HTTP_400_BAD_REQUEST)


"""
This class  (POST method) facilitates to retrieve Messages based on the keyword.
@Class_Name: ExploreByKeyword
@Params: keyword
"""


class ExploreByKeyword(APIView):
    @staticmethod
    def post(request):
        try:
            serializer = KeyWordSerializer(data=request.data)
            if serializer.is_valid() and serializer.data['keyword']:
                messages = MessageHolder.objects.filter(message__search=serializer.data['keyword'])
                data = itertools.groupby(messages, lambda record: record.user_id)
                messages_by_user = [(user, list(message_this_day)) for user, message_this_day in data]
                result = dict()
                for data in messages_by_user:
                    temp = []
                    for msg in data[1]:
                        temp.append(msg.message)
                    result[str(data[0].username)] = temp
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(exception="Bad Request", status=status.HTTP_400_BAD_REQUEST)
