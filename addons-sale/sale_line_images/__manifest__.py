# -*- coding: utf-8 -*-
{
    'name': "Sale Line Images",

    'summary': """
        -Adds Product images in sale order line.
    """,
    'description': """
        -Adds Product images in sale order line.
""",
    'author': "Palmate",
    'website': "www.palmate.in",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '15.0.0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/sale_views.xml',
        'report/report_sale_inherit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
