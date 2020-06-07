import django_filters
from django_filters import BaseInFilter, NumberFilter, NumericRangeFilter, CharFilter, DateTimeFromToRangeFilter, \
    IsoDateTimeFilter

from ethereum.models import TransactionRelationship, Account, Block


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass


class TransactionRelationshipFilter(django_filters.FilterSet):
    from_account = CharInFilter(field_name="from_account__public_key")
    to_account = CharInFilter(field_name="to_account__public_key")
    hash = CharInFilter(field_name="transaction__hash")
    block = NumberInFilter(field_name="block__number")
    miner = CharInFilter(field_name="block__miner__public_key")
    gas_price_max = NumberFilter(field_name="transaction__gas_price", lookup_expr="lte")
    gas_price_min = NumberFilter(field_name="transaction__gas_price", lookup_expr="gte")
    value_max = NumberFilter(field_name="transaction__value", lookup_expr="lte")
    value_min = NumberFilter(field_name="transaction__value", lookup_expr="gte")
    gas_max = NumberFilter(field_name="transaction__gas", lookup_expr="lte")
    gas_min = NumberFilter(field_name="transaction__gas", lookup_expr="gte")
    timestamp_max = IsoDateTimeFilter(field_name="block__timestamp", lookup_expr="lte")
    timestamp_min = IsoDateTimeFilter(field_name="block__timestamp", lookup_expr="gte")


    class Meta:
        model = TransactionRelationship
        fields = [
            "from_account",
            "to_account",
            "hash",
            "block",
            "miner",
            "gas_price_max",
            "gas_price_min",
            "value_max",
            "value_min",
            "gas_max",
            "gas_min",
            "timestamp_max",
            "timestamp_min",
        ]


class AccountFilter(django_filters.FilterSet):

    balance_in_wei = NumericRangeFilter(field_name="balance_in_wei")
    account = CharInFilter(field_name="public_key")

    class Meta:
        model = Account
        fields = [
            "balance_in_wei",
            "account",
        ]


class BlockFilter(django_filters.FilterSet):
    number = NumberInFilter(field_name="number")
    miner = CharInFilter(field_name="miner__public_key")

    class Meta:
        model = Block
        fields = [
            "number",
            "miner"
        ]