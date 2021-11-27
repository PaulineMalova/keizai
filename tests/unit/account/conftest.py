import pytest

from uuid import uuid4

from app.account.models import Account, AccountTransactionCategory, Ledger


@pytest.fixture
def account(session_user):
    def _account():
        return {
            "user_id": session_user.user_id,
            "created_by": str(uuid4()),
            "updated_by": str(uuid4()),
        }

    return _account


@pytest.fixture
def create_account(session_user, session):
    def _create_account():
        account = Account(
            user_id=session_user.user_id,
            created_by=str(uuid4()),
            updated_by=str(uuid4()),
        )
        session.add(account)
        session.commit()
        return account

    return _create_account


@pytest.fixture
def account_transaction_category(create_account):
    account = create_account()

    def _account_transaction_category():
        return {
            "account_id": account.account_id,
            "category_name": "Savings",
            "transaction_type": "SAVINGS",
            "created_by": str(uuid4()),
            "updated_by": str(uuid4()),
        }

    return _account_transaction_category


@pytest.fixture
def create_account_transaction_category(create_account, session):
    account = create_account()

    def _create_account_transaction_category(category_name, transaction_type):
        account_transaction_category = AccountTransactionCategory(
            account_id=account.account_id,
            category_name=category_name,
            transaction_type=transaction_type,
            created_by=str(uuid4()),
            updated_by=str(uuid4()),
        )
        session.add(account_transaction_category)
        session.commit()
        return account_transaction_category

    return _create_account_transaction_category


@pytest.fixture
def ledger(create_account_transaction_category):
    transaction_category = create_account_transaction_category("Rent", "DEBIT")
    transaction_category_id = (
        transaction_category.account_transaction_category_id
    )

    def _ledger():
        return {
            "account_id": transaction_category.account_id,
            "transaction_category_id": transaction_category_id,
            "amount": 5000,
            "transaction_cost": 36,
            "created_by": str(uuid4()),
            "updated_by": str(uuid4()),
            "source_account": "ACCOUNT",
        }

    return _ledger


@pytest.fixture
def create_ledger(create_account_transaction_category, session):
    transaction_category = create_account_transaction_category(
        "Electricity", "DEBIT"
    )
    transaction_category_id = (
        transaction_category.account_transaction_category_id
    )

    def _create_ledger():
        ledger = Ledger(
            account_id=transaction_category.account_id,
            transaction_category_id=transaction_category_id,
            amount=1000,
            transaction_cost=23,
            created_by=str(uuid4()),
            updated_by=str(uuid4()),
            source_account="SAVINGS_ACCOUNT"
        )
        session.add(ledger)
        session.commit()
        return ledger

    return _create_ledger
