from uuid import UUID
from typing import Optional

from app.base.input import BaseInput
from app.enums import TransactionTypeEnum, SourceAccountEnum


class AccountInput(BaseInput):
    user_id: UUID


class AccountTransactionCategoryInput(BaseInput):
    account_id: Optional[UUID]
    category_name: Optional[str]
    transaction_type: Optional[TransactionTypeEnum]


class LedgerInput(BaseInput):
    account_id: UUID
    transaction_category_id: UUID
    amount: float
    transaction_cost: float
    source_account: SourceAccountEnum
