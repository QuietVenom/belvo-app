import json
import uuid
from pprint import pprint

import requests
from decouple import config
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from requests.auth import HTTPBasicAuth

from belvo.client import Client
from belvo.enums import AccessMode


class BelvoService:
    def __init__(self):
        self.main_url = config("BELVO_URL")
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        self.auth = HTTPBasicAuth(config("BELVO_ID"), config("BELVO_SECRET"))
        self.client = Client(config("BELVO_ID"), config("BELVO_SECRET"), "sandbox")

    def get_all_institutions(self):
        client = self.client
        institution_list = client.Institutions.list()
        response = jsonable_encoder(institution_list)
        return JSONResponse(content=response)

        # url = self.main_url + "/api/institutions/"
        # response = requests.get(url, auth=self.auth, headers=self.headers)

        # if response.status_code == 200:
        #     json_compatible_item_data = jsonable_encoder(response)
        #     return JSONResponse(content=json_compatible_item_data)
        # else:
        #     print(response)
        #     raise HTTPException(401, "Invalid Credentials")

    def get_all_links(self):
        client = self.client
        links_list = client.Links.list()
        response = jsonable_encoder(links_list)
        return JSONResponse(content=response)

    def create_link(self, institution_name, inst_username, inst_pass):
        client = self.client
        link = client.Links.create(
            institution=institution_name,
            username=inst_username,
            password=inst_pass,
            access_mode=AccessMode.SINGLE
        )
        return link

    def retrieve_accounts(self, link):
        client = self.client
        accounts = client.Accounts.create(
            link=link,
            save_data=False
        )
        return accounts

    def get_transactions(self, link, date_from, date_to):
        client = self.client
        transactions = client.Transactions.create(
            link,
            date_from,
            date_to=date_to,
            save_data=False
        )
        return transactions

    def get_balance(self, link, date_from, date_to):
        client = self.client
        balances = client.Balances.create(
            link,
            date_from,
            date_to=date_to,
            save_data=False
        )
        return balances

    def get_owners(self, link):
        client = self.client
        owners = client.Owners.create(
            link,
            save_data=False
        )
        return owners
