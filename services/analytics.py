from io import StringIO
from msilib.schema import tables

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi.encoders import jsonable_encoder
import json


class BelvoAnalyze:
    @staticmethod
    def json_to_df(json_obj):
        df = pd.read_json(json_obj, orient='columns')
        return df

    @staticmethod
    def model_accounts(accounts_json):
        accounts_json = json.dumps(accounts_json)
        accounts_df = BelvoAnalyze.json_to_df(accounts_json)
        accounts = accounts_df.drop(['id', 'link', 'collected_at', 'type', 'agency', 'bank_product_id',
                    'internal_identification', 'credit_data', 'loan_data'], axis=1)
        return accounts

    @staticmethod
    def model_balances(balance_json):
        balance_json = json.dumps(balance_json)
        balance_df = BelvoAnalyze.json_to_df(balance_json)
        balance_df['value_date'] = pd.to_datetime(balance_df['value_date'])
        balance_table = balance_df.drop(['id', 'account', 'collected_at'], axis=1)
        balance_plot = balance_table['balance'].groupby(balance_table['value_date'].dt.to_period('M')).mean().plot(kind='bar')
        return balance_plot

    @staticmethod
    def model_owner(owner_json):
        owner_json = json.dumps(owner_json)
        owner_df = BelvoAnalyze.json_to_df(owner_json)
        owners_table = owner_df.drop(['id', 'link', 'created_at', 'collected_at'
                        , 'first_name', 'last_name', 'second_last_name'], axis=1)
        return owners_table

    @staticmethod
    def model_transactions(transactions_json):
        transactions_json = json.dumps(transactions_json)
        trans_df = BelvoAnalyze.json_to_df(transactions_json)
        trans_df['value_date'] = pd.to_datetime(trans_df['value_date'])
        transactions_table = trans_df.drop(['id', 'account', 'created_at', 'collected_at'
                            , 'accounting_date', 'observations', 'gig_data'], axis=1)
        transactions_table = transactions_table.sort_values(by=['value_date'])
        return transactions_table

    @staticmethod
    def plot_transactions(trans_table):
        flow_table = trans_table
        flow_table = flow_table.drop(['category', 'merchant', 'currency', 'description', 'internal_identification'
                                    , 'status', 'reference', 'balance'], axis=1)
        flow_table['inflow'] = flow_table['amount'].where(flow_table['type'] == 'INFLOW')
        flow_table['outflow'] = flow_table['amount'].where(flow_table['type'] == 'OUTFLOW')
        flow_table = flow_table.drop(['amount', 'type'], axis=1)
        flow_table = flow_table.groupby(flow_table['value_date'].dt.to_period('M')).sum()
        return BelvoAnalyze.belvo_plot(flow_table)

    @staticmethod
    def belvo_plot(table):
        financials_fig, ax = plt.subplots(figsize = (15,7.5))

        x = np.arange(len(table.index))
        width = 0.35

        inflow = ax.bar(x - width/2, table['inflow'], width, label='Inflow')
        outflow = ax.bar(x + width/2, table['outflow'], width, label='Outflow')
        behaviour = ax.plot(x, table['inflow'] - table['outflow'], 'o-', color='red', linewidth=3)

        ax.set_title('Financial Behaviour', fontsize = 25, fontweight = 'bold', pad = 25);
        ax.set_xlabel('Date', fontsize = 20, fontweight = 'bold', labelpad = 15)
        ax.set_ylabel('Inflow & Outflow', fontsize = 20, fontweight = 'bold', labelpad = 15)

        labels = table.index
        plt.xticks(x, labels, fontweight = 'bold', fontsize = 12, rotation = 90);

        return financials_fig
