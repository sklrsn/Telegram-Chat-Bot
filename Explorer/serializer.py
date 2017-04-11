from rest_framework import serializers

"""
@Class_Name: UserNameSerializer
@Params: username
"""


class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = ('username',)


"""
@Class_Name: DateSerializer
@Params: query_date
"""


class DateSerializer(serializers.Serializer):
    query_date = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = ('query_date',)


"""
@Class_Name: KeyWordSerializer
@Params: keyword
"""


class KeyWordSerializer(serializers.Serializer):
    keyword = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = ('keyword',)
