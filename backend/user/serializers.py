from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True)
    max_size = serializers.IntegerField(read_only=True)
    used_size = serializers.IntegerField(read_only=True)
    date_last_opt = serializers.DateTimeField(read_only=True)
    nickname = serializers.CharField()


    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance
