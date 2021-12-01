from app.base.controller import BaseController
from app.account.models import Account, AccountTransactionCategory, Ledger
from app.account.schemas import (
    AccountSchema,
    AccountTransactionCategorySchema,
    LedgerSchema,
)
from app.utils import get_or_create
from app.enums import TransactionTypeEnum


class AccountController(BaseController):
    model = Account
    schema = AccountSchema


class AccountTransactionCategoryController(BaseController):
    model = AccountTransactionCategory
    schema = AccountTransactionCategorySchema


class LedgerController(BaseController):
    model = Ledger
    schema = LedgerSchema

    @classmethod
    def perform_post(cls, session, data, schema):
        """Override base method to update account balance"""
        created, item = get_or_create(session, cls.model, schema, data)
        if created is True:
            update_account_balance(session, data)
        return created, item


def update_account_balance(session, data):
    transaction_category_id = data["transaction_category_id"]
    amount = data["amount"]
    account_id = data["account_id"]
    transaction_cost = data["transaction_cost"]
    source_account = data["source_account"]
    account = session.query(Account).get(account_id)
    account_balance = account.account_balance
    account_savings = account.account_savings
    cash_balance = account.cash_balance
    transaction_category = session.query(AccountTransactionCategory).get(
        transaction_category_id
    )
    transaction_type = transaction_category.transaction_type
    if transaction_type == TransactionTypeEnum.SAVINGS:
        account_savings += amount
        if source_account == "SAVINGS_ACCOUNT":
            account_savings -= transaction_cost + amount
        elif source_account == "ACCOUNT":
            total_deduction = amount + transaction_cost
            account_balance -= total_deduction
        elif source_account == "CASH":
            total_deduction = amount + transaction_cost
            cash_balance -= total_deduction

    elif transaction_type == TransactionTypeEnum.DEBIT:
        total_deduction = amount + transaction_cost
        if source_account == "ACCOUNT":
            account_balance -= total_deduction
        elif source_account == "SAVINGS_ACCOUNT":
            account_savings -= total_deduction
        elif source_account == "CASH":
            cash_balance -= total_deduction

    elif transaction_type == TransactionTypeEnum.ACCOUNT_CREDIT:
        account_balance += amount
        if source_account == "SAVINGS_ACCOUNT":
            account_savings -= amount + transaction_cost
        elif source_account == "ACCOUNT":
            account_balance -= transaction_cost + amount
        elif source_account == "CASH":
            cash_balance -= transaction_cost + amount

    elif transaction_type == TransactionTypeEnum.CASH_CREDIT:
        cash_balance += amount
        if source_account == "SAVINGS_ACCOUNT":
            account_savings -= amount + transaction_cost
        elif source_account == "ACCOUNT":
            account_balance -= transaction_cost + amount
        elif source_account == "CASH":
            cash_balance -= transaction_cost + amount

    balance_update_payload = {
        "account_balance": account_balance,
        "account_savings": account_savings,
        "cash_balance": cash_balance,
        "updated_by": "System",
    }

    AccountController.update_record(
        session, balance_update_payload, account_id
    )

    return {"success": True}
