from rest_framework.serializers import ModelSerializer

from ledgers.models import Ledger


class LedgerSerializer(ModelSerializer):
    class Meta:
        exclude = ("user",)
        model = Ledger
