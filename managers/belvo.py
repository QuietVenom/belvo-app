import os

from constants import TEMP_FILE_FOLDER
from db import database
from models import user
from services.analytics import BelvoAnalyze
from services.belvo import BelvoService
from jinja2 import Environment, FileSystemLoader

belvo = BelvoService()
analyze = BelvoAnalyze()


class BelvoManager:
    @staticmethod
    def get_institutions():
        response = belvo.get_all_institutions()
        return response

    @staticmethod
    def get_all_links():
        response = belvo.get_all_links()
        return response

    @staticmethod
    def create_link(institution, username, password):
        response = belvo.create_link(institution, username, password)
        return response

    @staticmethod
    def retrieve_accounts(link):
        response = belvo.retrieve_accounts(link)
        return response

    @staticmethod
    def transactions(link, date_from, date_to):
        response = belvo.get_transactions(link, date_from, date_to)
        return response

    @staticmethod
    def get_balance(link, date_from, date_to):
        response = belvo.get_balance(link, date_from, date_to)
        return response

    @staticmethod
    def get_owners(link):
        response = belvo.get_owners(link)
        return response

    @staticmethod
    async def get_all_users():
        q = user.select()
        return await database.fetch_all(q)

    @staticmethod
    def belvo_dashboard(link, date_from, date_to):
        env = Environment(loader=FileSystemLoader('./dashboard'))
        template = env.get_template('dashboard.html')

        owners = belvo.get_owners(link)
        balance = belvo.get_balance(link, date_from, date_to)
        transaction = belvo.get_transactions(link, date_from, date_to)
        accounts = belvo.retrieve_accounts(link)

        owner_table = analyze.model_owner(owners)
        balance_plot = analyze.model_balances(balance)
        trans_table = analyze.model_transactions(transaction)
        accounts_table = analyze.model_accounts(accounts)
        trans_plot = analyze.plot_transactions(trans_table)

        path = os.path.join(TEMP_FILE_FOLDER, 'dashboard')
        isExist = os.path.exists(path)
        if not isExist:
            os.mkdir(path)
            print("The new directory is created!")

        balance_plot.figure.savefig(path + '/balance_plot.png')
        trans_plot.savefig(path + '/trans_plot.png')
        trans_html = trans_table.to_html()
        owner_html = owner_table.to_html()
        accounts_html = accounts_table.to_html()

        template_vars = {'transactions': trans_html, 'owners': owner_html, 'accounts': accounts_html}
        html_out = template.render(template_vars)
        html_file = open(path + '/dashboard.html', 'w')
        html_file.write(html_out)
        html_file.close()
        return print('Check your TEMP_FILES')
