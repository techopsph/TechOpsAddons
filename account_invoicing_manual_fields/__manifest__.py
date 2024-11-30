# -*- coding: utf-8 -*-
{
    'name': "Sales Invoice Manual Fields",
    'summary': "Additional Text Fields and Relation Fields for Manual Sales Invoicing",
    'description': """
        Additional Text Fields and Relation Fields for Manual Sales Invoicing
        Custom Invoice Fields
        Sales Invoice Booklet
    """,
    'author': "Tech Ops PH",
    'website': "https://techops.ph",
    'category': 'Invoicing',
    'version': '16.0',
    'depends': ['account'],

    # always loaded
    'data': [
        'views/account_move.xml',
    ],
}

