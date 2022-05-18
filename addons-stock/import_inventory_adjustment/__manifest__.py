# -*- coding: utf-8 -*-
{
    'name': "Import Inventory Adjustment",

    'summary': """Import Inventory Adjustment""",

    'description': """
        Import Inventory Adjustment
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # for the full list
    'category': 'Stock',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_inventory_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
