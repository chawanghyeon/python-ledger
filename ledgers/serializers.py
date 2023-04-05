from rest_framework.serializers import ModelSerializer

from ledgers.models import Ledger


class LedgerSerializer(ModelSerializer):
    # type = serializers.CharField(required=False)

    class Meta:
        exclude = ("user",)
        model = Ledger
