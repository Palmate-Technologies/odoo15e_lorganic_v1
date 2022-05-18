# -*- coding: utf-8 -*-
{
    'name': "Account Move Line Images",

    'summary': " This module show the product image in account.move.line "
               "and also show the account invoices report",

    'description': """""",
    'author': "Palmate",
    'category': 'Account',
    'version': '15.0',
    'website': "https://www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['account'],

    'data': [
        'views/account_views.xml',
        # 'report/report_invoices_inherit.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
