from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserNameSerializer, DateSerializer
from WebCrawler.models import ApplicationUser, MessageHolder
from datetime import datetime
import itertools


class ExploreByUserName(APIView):
    def post(self, request):
        try:
            serializer = UserNameSerializer(data=request.data)
            if serializer.is_valid():
                app_user = ApplicationUser.objects.get(username=serializer.data['username'])
                messages = MessageHolder.objects.filter(user_id=app_user)
                result = dict()
                data = []
                for msg in messages:
                    data.append(str(msg.message_id) + "." + msg.message)
                result["messages"] = data
                return Response(result, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_403_FORBIDDEN)


class ExploreByDate(APIView):
    def post(self, request):
        try:
            serializer = DateSerializer(data=request.data)
            if serializer.is_valid():
                query_date = datetime.strptime(serializer.data['query_date'],
                                               "%Y-%m-%d %H:%M:%S")
                messages = MessageHolder.objects.filter(message_date__year=query_date.year,
                                                        message_date__month=query_date.month,
                                                        message_date__day=query_date.day)

                data = itertools.groupby(messages, lambda record: record.user_id)
                messages_by_user = [(user, list(message_this_day)) for user, message_this_day in data]
                result = dict()
                for data in messages_by_user:
                    temp = []
                    for msg in data[1]:
                        temp.append(str(msg.message_id) + "." + msg.message)
                    result[str(data[0].username)] = temp
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
