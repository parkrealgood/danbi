from rest_framework import serializers

from user.models import User, Team


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data.get('email')
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return user


class TeamBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class UserBaseSerializer(serializers.ModelSerializer):
    team = TeamBaseSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'team']
