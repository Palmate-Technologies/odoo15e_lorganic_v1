# -*- coding: utf-8 -*-
{
    'name': "Import Pos Orders Changes",

    'summary': """
        -Import POS orders using odoo's file import feature.\n
        -Make readonly fields Editable so that those can be imported using file import.
    
""",

    'description': """
        -Import POS orders using odoo's file import feature. \n
        -Make readonly fields Editable so that those can be imported using file import.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0.0.1',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_pos_order_views.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
