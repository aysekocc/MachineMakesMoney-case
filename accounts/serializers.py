
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated):
        email = validated.get('email')
        password = validated.get('password')
        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()
        return user
