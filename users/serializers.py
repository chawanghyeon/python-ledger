from rest_framework.serializers import CharField, ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        fields = "__all__"
        model = User
