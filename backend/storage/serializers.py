from rest_framework import serializers
from storage.models import Catalogue


class CatalogueSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    is_file = serializers.ReadOnlyField()
    is_shared = serializers.ReadOnlyField()
    date_modified = serializers.ReadOnlyField()

    name = serializers.CharField(required=False, default='新建文件夹')
    extension = serializers.CharField(required=False)

    class Meta:
        model = Catalogue
        fields = (
            'id', 'name', 'is_file', 'is_shared',
            'date_modified', 'extension'
        )

class BreadcrumbsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Catalogue
        fields = ('id', 'name')
