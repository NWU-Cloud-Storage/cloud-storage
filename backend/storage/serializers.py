from rest_framework import serializers
from storage.models import Identifier, Storage, Membership


class CatalogueSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    is_file = serializers.ReadOnlyField()
    is_shared = serializers.ReadOnlyField()
    date_modified = serializers.ReadOnlyField()

    name = serializers.CharField(required=False, default='新建文件夹')
    extension = serializers.CharField(required=False)
    size = serializers.ReadOnlyField(source="my_file.size")
    owner = serializers.PrimaryKeyRelatedField(source='owner.nickname', read_only=True)

    class Meta:
        model = Identifier
        fields = (
            'id', 'name', 'is_file', 'is_shared',
            'date_modified', 'extension', 'size', 'owner'
        )


class BreadcrumbsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Identifier
        fields = ('id', 'name')


class StorageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='root_identifier.name')
    storage_id = serializers.ReadOnlyField(source='id')
    root_folder_id = serializers.PrimaryKeyRelatedField(source='root_identifier', read_only=True)
    created_time = serializers.ReadOnlyField()
    is_personal_storage = serializers.ReadOnlyField()
    default_permission = serializers.CharField()

    def validate(self, data):
        if data.get('default_permission') is None and \
                data.get('root_identifier') is None:
            raise serializers.ValidationError("must fill name or default_permission")
        return data

    def update(self, instance, validated_data):
        identifier = instance.root_identifier
        identifier.name = validated_data['root_identifier']['name']
        identifier.save()
        return instance

    class Meta:
        model = Storage
        fields = ('name', 'storage_id', 'root_folder_id', 'created_time',
                  'is_personal_storage', 'default_permission')


class StorageMemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    nickname = serializers.ReadOnlyField(source='user.nickname')
    permission = serializers.CharField()

    class Meta:
        model = Membership
        fields = ('username', 'nickname', 'permission')
