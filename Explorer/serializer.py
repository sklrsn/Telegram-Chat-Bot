from rest_framework import serializers


class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = ('username',)