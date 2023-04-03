from rest_framework.serializers import ModelSerializer

from ledgers.models import Ledger


class LedgerSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ledger
        depth = 1
