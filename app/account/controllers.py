from app.base.controller import BaseController
from app.account.models import Account, AccountTransactionCategory, Ledger
from app.account.schemas import (
    AccountSchema,
    AccountTransactionCategorySchema,
    LedgerSchema,
)


class AccountController(BaseController):
    model = Account
    schema = AccountSchema


class AccountTransactionCategoryController(BaseController):
    model = AccountTransactionCategory
    schema = AccountTransactionCategorySchema


class LedgerController(BaseController):
    model = Ledger
    schema = LedgerSchema
