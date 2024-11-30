# -*- coding: utf-8 -*-
{
    'name': "Counter Receipts",
    'summary': "Counter Receipts for Customer Invoices or Vendor Bills",
    'description': """
        Counter Receipts for Customer Invoices or Vendor Bills
    """,
    'author': "Tech Ops PH",
    'website': "https://techops.ph",
    'category': 'Invoicing',
    'version': '16.0',
    'depends': ['account_invoicing_manual_fields'],

    # always loaded
    'data': [
        'data/ir_actions_report.xml',
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'reports/counter_receipts.xml',
        'views/counter_receipts.xml',
        'views/account_move.xml',
        'views/menu_actions.xml',
    ],
}

