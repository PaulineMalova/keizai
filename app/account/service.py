import uuid

from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session

from app.database import create_session
from app.account.controllers import (
    AccountController,
    AccountTransactionCategoryController,
    LedgerController,
)
from app.account.input import (
    AccountInput,
    AccountTransactionCategoryInput,
    LedgerInput,
)
from app.auth import authorize


session: Session = create_session()

router = APIRouter(tags=["account"])

####################################################################
#                         User account
####################################################################


@router.get("/accounts")
def get_accounts(request: Request):
    result = AccountController.as_view(session, request)
    return result


@router.post("/accounts")
def create_account(
    account: AccountInput, request: Request, response: Response
):
    result = AccountController.as_view(
        session, request, item=account, response=response
    )
    return result


@router.get("/accounts/{account_id}")
def get_account(request: Request, account_id: uuid.UUID, response: Response):
    result = AccountController.as_view(
        session, request, pk=account_id, response=response
    )
    return result


@router.delete("/accounts/{account_id}")
@authorize
def delete_account(request: Request, account_id: str, response: Response):
    result = AccountController.as_view(
        session, request, pk=account_id, response=response
    )
    return result


####################################################################
#                Account Transaction Category
####################################################################


@router.get("/account-transaction-categories")
def get_account_transaction_categories(request: Request):
    result = AccountTransactionCategoryController.as_view(session, request)
    return result


@router.post("/account-transaction-categories")
@authorize
def create_account_transaction_category(
    account_transaction_category: AccountTransactionCategoryInput,
    request: Request,
    response: Response,
):
    result = AccountTransactionCategoryController.as_view(
        session, request, item=account_transaction_category, response=response
    )
    return result


@router.get(
    "/account-transaction-categories/{account_transaction_category_id}"
)
def get_account_transaction_category(
    request: Request,
    account_transaction_category_id: uuid.UUID,
    response: Response,
):
    result = AccountTransactionCategoryController.as_view(
        session, request, pk=account_transaction_category_id, response=response
    )
    return result


@router.put(
    "/account-transaction-categories/{account_transaction_category_id}"
)
@authorize
def update_account_transaction_category(
    account_transaction_category: AccountTransactionCategoryInput,
    request: Request,
    account_transaction_category_id: str,
    response: Response,
):
    result = AccountTransactionCategoryController.as_view(
        session,
        request,
        account_transaction_category,
        pk=account_transaction_category_id,
        response=response,
    )
    return result


@router.delete(
    "/account-transaction-categories/{account_transaction_category_id}"
)
@authorize
def delete_account_transaction_category(
    request: Request, account_transaction_category_id: str, response: Response
):
    result = AccountTransactionCategoryController.as_view(
        session, request, pk=account_transaction_category_id, response=response
    )
    return result


####################################################################
#                            Ledger
####################################################################


@router.get("/transactions")
def get_transactions(request: Request):
    result = LedgerController.as_view(session, request)
    return result


@router.post("/transactions")
@authorize
def create_transaction(
    ledger: LedgerInput, request: Request, response: Response
):
    result = LedgerController.as_view(
        session, request, item=ledger, response=response
    )
    return result


@router.get("/transactions/{ledger_id}")
def get_transaction(
    request: Request, ledger_id: uuid.UUID, response: Response
):
    result = LedgerController.as_view(
        session, request, pk=ledger_id, response=response
    )
    return result
