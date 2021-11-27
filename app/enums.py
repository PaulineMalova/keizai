from enum import Enum


class TransactionTypeEnum(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    SAVINGS = "SAVINGS"


class SourceAccountEnum(Enum):
    ACCOUNT = "ACCOUNT"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT"
    EXTERNAL = "EXTERNAL"
