from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField()
    max_size = serializers.ReadOnlyField()
    used_size = serializers.ReadOnlyField()
    date_last_opt = serializers.ReadOnlyField()
    nickname = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'max_size', 'used_size', 'date_last_opt')
