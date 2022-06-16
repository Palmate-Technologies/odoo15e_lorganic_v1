{
    'name': 'Print Label Custom',
    'summary': """""",
    'description': """""",
    'category': 'Base',
    'version': '15.0.0.1',
    'author': 'palmate',
    'website': "https://www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['base', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/label_view.xml',
        'report/label.xml',
        'report/product_label.xml',

    ],

    'images': ['static/description/banner.png'],


    'installable': True,
    'auto_install': False,
    'application': False,
}
