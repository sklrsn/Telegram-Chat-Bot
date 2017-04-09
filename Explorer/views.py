from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserNameSerializer
from WebCrawler.models import ApplicationUser, MessageHolder


class ExploreByUserName(APIView):
    def post(self, request):
        try:
            serializer = UserNameSerializer(data=request.data)
            if serializer.is_valid():
                user_name = serializer.data['username']
                app_user = ApplicationUser.objects.get(username=user_name)
                messages = MessageHolder.objects.filter(user_id=app_user)
                result = dict()
                inps = []
                for msg in messages:
                    inps.append(msg.message)
                result["messages"] = inps
                print(messages)
                return Response(result, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_403_FORBIDDEN)
