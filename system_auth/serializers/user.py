# RestFrameWork Import
from rest_framework import serializers

# Model Import
from ..models import CustomUser

# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"