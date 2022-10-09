from lib2to3.pytree import Base
from typing import List, Optional

from fastapi import APIRouter, Depends

from managers.belvo import BelvoManager
from managers.auth import is_user, oauth2_scheme
from schemas.response.user import UserOut
from schemas.base import BaseLink, BaseAccount, BaseTransaction


router = APIRouter(tags=["Belvo"])

@router.get(
    "/users/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)],
    response_model=List[UserOut])
async def get_all_users():
    return await BelvoManager.get_all_users()


@router.get(
    "/all_institutions/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def get_all_institutions():
    return BelvoManager.get_institutions()


@router.get(
    "/all_links/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def get_all_links():
    return BelvoManager.get_all_links()


@router.post(
    "/new_link/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def create_link(new_link: BaseLink):
    data = new_link.dict()
    return BelvoManager.create_link(data["institution"], data["username"], data["password"])


@router.post(
    "/accounts/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def retrieve_accounts(accounts: BaseAccount):
    data = accounts.dict()
    return BelvoManager.retrieve_accounts(data["link"])


@router.post(
    "/transactions/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def transactions(transaction: BaseTransaction):
    data = transaction.dict()
    return BelvoManager.transactions(data["link"], data["date_from_YYYYMMDD"], data["date_to_YYYYMMDD"])


@router.post(
    "/balances/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def balances(balance: BaseTransaction):
    data = balance.dict()
    return BelvoManager.get_balance(data["link"], data["date_from_YYYYMMDD"], data["date_to_YYYYMMDD"])


@router.post(
    "/owners/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)])
def get_owners(owners: BaseAccount):
    data = owners.dict()
    return BelvoManager.get_owners(data["link"])


@router.post(
    "/dashboard/",
    dependencies=[Depends(oauth2_scheme), Depends(is_user)],
    status_code=201)
def run_dashboard(dash: BaseTransaction):
    data = dash.dict()
    return BelvoManager.belvo_dashboard(data["link"], data["date_from_YYYYMMDD"], data["date_to_YYYYMMDD"])
