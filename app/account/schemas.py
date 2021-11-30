from marshmallow import fields
from marshmallow_enum import EnumField

from app.base.schema import BaseSchema
from app.account.models import Account, AccountTransactionCategory, Ledger
from app.enums import TransactionTypeEnum, SourceAccountEnum


class AccountSchema(BaseSchema):
    account_id = fields.UUID(dump_only=True)
    user_id = fields.UUID(
        required=True, error_messages={"required": "User id is required"}
    )
    account_balance = fields.Float(allow_nan=True)
    account_savings = fields.Float(allow_nan=True)
    # cash_balance = fields.Float(allow_nan=True)

    class Meta(BaseSchema.Meta):
        model = Account
        unique_fields = ["user_id"]


class AccountTransactionCategorySchema(BaseSchema):
    account_transaction_category_id = fields.UUID(dump_only=True)
    account_id = fields.UUID(
        required=True, error_messages={"required": "Account id is required"}
    )
    category_name = fields.Str(
        required=True, error_messages={"required": "Category name is required"}
    )
    transaction_type = EnumField(
        TransactionTypeEnum,
        required=True,
        error_messages={"required": "Transaction type is required"},
    )

    class Meta(BaseSchema.Meta):
        model = AccountTransactionCategory
        unique_fields = ["category_name", "account_id", "transaction_type"]


class LedgerSchema(BaseSchema):

    ledger_id = fields.UUID(dump_only=True)
    account_id = fields.UUID(
        required=True, error_messages={"required": "Account id is required"}
    )
    transaction_category_id = fields.UUID(
        required=True,
        error_messages={"required": "Transaction category id is required"},
    )
    amount = fields.Float(
        required=True, error_messages={"required": "Amount is required"}
    )
    transaction_cost = fields.Float(
        required=True,
        error_messages={"required": "Transaction cost is required"},
    )
    source_account = EnumField(
        SourceAccountEnum,
        required=True,
        error_messages={"required": "Source account is required"},
    )
    account = fields.Nested(AccountSchema)
    transaction_category = fields.Nested(AccountTransactionCategorySchema)

    class Meta(BaseSchema.Meta):
        model = Ledger
