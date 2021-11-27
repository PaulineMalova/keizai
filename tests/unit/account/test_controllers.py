import json

from uuid import uuid4

from app.account.controllers import (
    AccountController,
    AccountTransactionCategoryController,
    LedgerController,
)
from app.account.models import Account


class TestAccount:
    @staticmethod
    def test_can_get_multiple_accounts(session, create_account):
        create_account()
        accounts = json.loads(AccountController.fetch_records(session))
        if len(accounts) != 1:
            raise AssertionError()

    @staticmethod
    def test_can_add_account(session, account):
        result = json.loads(AccountController.post_record(session, account()))
        if result["account_id"] is None:
            raise AssertionError()

    @staticmethod
    def test_can_update_account(session, create_account):
        new_account = create_account()
        updated_account = json.loads(
            AccountController.update_record(
                session, {"is_active": False}, new_account.account_id
            )
        )
        if updated_account["is_active"] is not False:
            raise AssertionError()

    @staticmethod
    def test_can_get_account(session, create_account):
        new_account = create_account()
        account = json.loads(
            AccountController.fetch_records(session, pk=new_account.account_id)
        )
        if account["account_id"] != str(new_account.account_id):
            raise AssertionError()

    @staticmethod
    def test_can_delete_account(session, create_account):
        new_account = create_account()
        deleted_response = json.loads(
            AccountController.soft_delete(
                session, pk=new_account.account_id, user_id=str(uuid4())
            )
        )
        if deleted_response["deleted"] is not True:
            raise AssertionError()


class TestAccountTransactionCategory:
    @staticmethod
    def test_can_get_multiple_account_transaction_categories(
        session, create_account_transaction_category
    ):
        create_account_transaction_category("Water", "DEBIT")
        create_account_transaction_category("Airtime", "DEBIT")
        account_transaction_categories = json.loads(
            AccountTransactionCategoryController.fetch_records(session)
        )
        if len(account_transaction_categories) != 2:
            raise AssertionError()

    @staticmethod
    def test_can_add_account_transaction_category(
        session, account_transaction_category
    ):
        result = json.loads(
            AccountTransactionCategoryController.post_record(
                session, account_transaction_category()
            )
        )
        if result["account_transaction_category_id"] is None:
            raise AssertionError()

    @staticmethod
    def test_can_update_account_transaction_category(
        session, create_account_transaction_category
    ):
        new_transaction_category = create_account_transaction_category(
            "Food", "DEBIT"
        )
        updated_transaction_category = json.loads(
            AccountTransactionCategoryController.update_record(
                session,
                {"category_name": "Foodstuff"},
                new_transaction_category.account_transaction_category_id,
            )
        )
        if updated_transaction_category["category_name"] != "Foodstuff":
            raise AssertionError()

    @staticmethod
    def test_can_get_account_transaction_category(
        session, create_account_transaction_category
    ):
        new_transaction_category = create_account_transaction_category(
            "Food", "DEBIT"
        )
        transaction_category = json.loads(
            AccountTransactionCategoryController.fetch_records(
                session,
                pk=new_transaction_category.account_transaction_category_id,
            )
        )
        if transaction_category["account_transaction_category_id"] != str(
            new_transaction_category.account_transaction_category_id
        ):
            raise AssertionError()

    @staticmethod
    def test_can_delete_account_transaction_category(
        session, create_account_transaction_category
    ):
        new_transaction_category = create_account_transaction_category(
            "Food", "DEBIT"
        )
        deleted_response = json.loads(
            AccountTransactionCategoryController.soft_delete(
                session,
                pk=new_transaction_category.account_transaction_category_id,
                user_id=str(uuid4()),
            )
        )
        if deleted_response["deleted"] is not True:
            raise AssertionError()


class TestLedger:
    @staticmethod
    def test_can_get_multiple_ledgers(session, create_ledger):
        for _ in range(5):
            create_ledger()
        ledgers = json.loads(LedgerController.fetch_records(session))
        if len(ledgers) != 5:
            raise AssertionError()

    @staticmethod
    def test_can_add_ledger(session, ledger):
        result = json.loads(LedgerController.post_record(session, ledger()))
        if result["ledger_id"] is None:
            raise AssertionError()

    @staticmethod
    def test_can_update_account_balances_accurately_with_debit_transaction(
        session, create_account_transaction_category, ledger
    ):
        transaction_category = create_account_transaction_category(
            "Toiletries", "DEBIT"
        )
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger = ledger()
        ledger[
            "transaction_category_id"
        ] = transaction_category.account_transaction_category_id
        ledger["amount"] = 3500
        transaction_cost = ledger["transaction_cost"]

        # With the source being user's account
        ledger["source_account"] = "ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_balance"]
            != (account.account_balance - (3500 + transaction_cost))
            or result["account"]["account_savings"] != account.account_savings
        ):
            raise AssertionError()

        # With the source being user's savings account
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "SAVINGS_ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_savings"]
            != (account.account_savings - (3500 + transaction_cost))
            or result["account"]["account_balance"] != account.account_balance
        ):
            raise AssertionError()

        # With the source being external (unaccounted for in this case)
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "EXTERNAL"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_savings"] != account.account_savings
            or result["account"]["account_balance"] != account.account_balance
        ):
            raise AssertionError()

    @staticmethod
    def test_can_update_account_balances_accurately_with_credit_transaction(
        session, create_account_transaction_category, ledger
    ):
        transaction_category = create_account_transaction_category(
            "Investment Interest", "CREDIT"
        )
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger = ledger()
        ledger[
            "transaction_category_id"
        ] = transaction_category.account_transaction_category_id
        ledger["amount"] = 1000

        # With the source being external
        ledger["source_account"] = "EXTERNAL"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_balance"]
            != (account.account_balance + 1000)
            or result["account"]["account_savings"] != account.account_savings
        ):
            raise AssertionError()

        # With the source being user's savings account
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "SAVINGS_ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_savings"]
            != (account.account_savings - (1000 + ledger["transaction_cost"]))
            or result["account"]["account_balance"]
            != account.account_balance + 1000
        ):
            raise AssertionError()

        # With the source being user's account
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_balance"]
            != (account.account_balance - (ledger["transaction_cost"]))
            or result["account"]["account_savings"] != account.account_savings
        ):
            raise AssertionError()

    @staticmethod
    def test_can_update_account_balances_accurately_with_savings_transaction(
        session, create_account_transaction_category, ledger
    ):
        transaction_category = create_account_transaction_category(
            "Sacco Saving", "SAVINGS"
        )
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger = ledger()
        ledger[
            "transaction_category_id"
        ] = transaction_category.account_transaction_category_id
        ledger["amount"] = 3500

        # With the source being external
        ledger["source_account"] = "EXTERNAL"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_balance"] != (account.account_balance)
            or result["account"]["account_savings"]
            != account.account_savings + 3500
        ):
            raise AssertionError()

        # With the source being user's savings account
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "SAVINGS_ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_savings"]
            != (account.account_savings - ledger["transaction_cost"])
            or result["account"]["account_balance"] != account.account_balance
        ):
            raise AssertionError()

        # With the source being user's account
        account = (
            session.query(Account.account_balance, Account.account_savings)
            .filter_by(account_id=transaction_category.account_id)
            .first()
        )
        ledger["source_account"] = "ACCOUNT"
        result = json.loads(LedgerController.post_record(session, ledger))
        if (
            result["account"]["account_balance"]
            != (account.account_balance - (3500 + ledger["transaction_cost"]))
            or result["account"]["account_savings"]
            != account.account_savings + 3500
        ):
            raise AssertionError()

    @staticmethod
    def test_can_update_ledger(session, create_ledger):
        new_ledger = create_ledger()
        updated_ledger = json.loads(
            LedgerController.update_record(
                session, {"amount": 50}, new_ledger.ledger_id
            )
        )
        if updated_ledger["amount"] != 50:
            raise AssertionError()

    @staticmethod
    def test_can_get_ledger(session, create_ledger):
        new_ledger = create_ledger()
        ledger = json.loads(
            LedgerController.fetch_records(session, pk=new_ledger.ledger_id)
        )
        if ledger["ledger_id"] != str(new_ledger.ledger_id):
            raise AssertionError()

    @staticmethod
    def test_can_delete_ledger(session, create_ledger):
        new_ledger = create_ledger()
        deleted_response = json.loads(
            LedgerController.soft_delete(
                session, pk=new_ledger.ledger_id, user_id=str(uuid4())
            )
        )
        if deleted_response["deleted"] is not True:
            raise AssertionError()
