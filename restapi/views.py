from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from ethereum.models import Account, TransactionRelationship, Block
from restapi.serializers import AccountSerializer, BlockSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TransactionRelationship.objects.all()
    serializer_class = AccountSerializer


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
