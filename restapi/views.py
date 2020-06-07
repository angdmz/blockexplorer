# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from ethereum.models import Account, TransactionRelationship, Block, SmartContract
from restapi.filters import TransactionRelationshipFilter
from restapi.serializers import AccountSerializer, BlockSerializer, TransactionSerializer, SmartContractSerializer, \
    TransactionRetrieveSerializer, AccountRetrieveSerializer


class GetSerializerClassMixin(object):

    serializer_action_classes = dict()

    def get_serializer_class(self):
        """
        A class which inhertis this mixins should have variable
        `serializer_action_classes`.
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class SampleViewSet(viewsets.ViewSet):
            serializer_class = DocumentSerializer
            serializer_action_classes = {
               'upload': UploadDocumentSerializer,
               'download': DownloadDocumentSerializer,
            }
            @action
            def upload:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class AccountViewSet(GetSerializerClassMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'public_key'
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    serializer_action_classes = {
        'list': AccountSerializer,
        'retrieve': AccountRetrieveSerializer
    }


class TransactionViewSet(GetSerializerClassMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TransactionRelationship.objects.all().select_related('transaction', 'from_account', 'to_account', 'block', 'receipt')
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = [""]
    serializer_class = TransactionSerializer
    lookup_field = "hash"
    serializer_action_classes = {
        'list': TransactionSerializer,
        'retrieve': TransactionRetrieveSerializer
    }
    filter_class = TransactionRelationshipFilter


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    queryset = Block.objects.all().select_related('miner')
    serializer_class = BlockSerializer
    lookup_field = "block_number"


class SmartContractViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    queryset = SmartContract.objects.all()
    serializer_class = SmartContractSerializer
    lookup_field = "public_key"
