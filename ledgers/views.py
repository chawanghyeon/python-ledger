from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response

from ledgers.models import Ledger
from ledgers.serializers import LedgerSerializer


class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()

    def create(self, request: HttpRequest) -> Response:
        serializer = LedgerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, type_id=request.data["type_id"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)
