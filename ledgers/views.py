from rest_framework import viewsets

from ledgers.models import Ledger
from ledgers.serializers import LedgerSerializer


class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()
