from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from ethereum.models import Account, TransactionRelationship
from restapi.serializers import AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = TransactionRelationship.objects.all().distinct('from_account')
    serializer_class = AccountSerializer