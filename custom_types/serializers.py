from rest_framework.serializers import ModelSerializer

from custom_types.models import CustomType


class CustomTypeSerializer(ModelSerializer):
    class Meta:
        exclude = ("user",)
        model = CustomType
        depth = 1
