from enum import Enum


class TransactionTypeEnum(Enum):
    ACCOUNT_CREDIT = "ACCOUNT_CREDIT"
    CASH_CREDIT = "CASH_CREDIT"
    DEBIT = "DEBIT"
    SAVINGS = "SAVINGS"


class SourceAccountEnum(Enum):
    ACCOUNT = "ACCOUNT"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT"
    EXTERNAL = "EXTERNAL"
    CASH = "CASH"
