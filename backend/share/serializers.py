from rest_framework import serializers
from share.models import Share


class ShareSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    expiration = serializers.ReadOnlyField()
    is_unlimited = serializers.ReadOnlyField()

    class Meta:
        model = Share
        fields = ('url', 'expiration', 'is_unlimited')
