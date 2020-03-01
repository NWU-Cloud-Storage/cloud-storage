from rest_framework import serializers
from .models import Group, MembershipTmp, Intention


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    num_of_members = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'num_of_members')

class MyGroupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='group.pk')
    num_of_members = serializers.ReadOnlyField(source='group.num_of_members')
    permission = serializers.ChoiceField(MembershipTmp.PERMISSIONS, required=False)
    name = serializers.CharField(source='group.name', required=False)

    class Meta:
        model = MembershipTmp
        fields = ('id', 'name', 'num_of_members', 'permission')


class GroupMemberSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(read_only=True, source='user.nickname')
    username = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = MembershipTmp
        fields = ('username', 'nickname', 'permission')

class IntentionSerializer(serializers.ModelSerializer):

    group_id = serializers.ReadOnlyField(source='group.pk')
    group_name = serializers.ReadOnlyField(source='group.name')
    username = serializers.ReadOnlyField(source='user.username')
    nickname = serializers.ReadOnlyField(source='user.nickname')
    date_intended = serializers.ReadOnlyField()

    class Meta:
        model = Intention
        fields = ('group_id', 'group_name', 'username', 'nickname', 'date_intended')
