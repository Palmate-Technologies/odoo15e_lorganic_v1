{
    'name': 'POS Arabic Receipt',
    'version': '15.0.0.4',
    'sequence': 1,
    'summary': 'Pierce PPA',
    'description': """
        POS receipt customization for arabic labels.
    """,
    'author': 'Palmate',
    'website': 'www.palmate.in',
    'sequence': 1,
    'license': 'LGPL-3',
    'images': [
        # 'images/main_screenshot.png',
    ],
    'depends': ['point_of_sale',
                'l10n_sa_pos',
                ],
    'data': [
        'views/pos_assets_common.xml',
    ],

    'assets': {
        'web.assets_qweb': [
            "pos_receipt_arabic/static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml",
        ],
        # 'point_of_sale.assets': [
        #     'pos_receipt_arabic/static/src/js/pos_custom.js',
        # ]
    },

    # 'qweb': [
    #     'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
    # ],
    'demo': [
    ],
    'installable': True,
}
