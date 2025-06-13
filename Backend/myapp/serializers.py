from rest_framework import serializers
from .models import CustomUser, UserDetails


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = ['id', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'user', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id']
