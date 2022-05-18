# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Custom KSA Invoice',
    'version': '1.0.0.1',
    'summary': """""",
    'description': """""",
    'category': 'Base',
    'author': 'palmate',
    'website': "",
    'license': 'AGPL-3',

    'depends': ['l10n_sa', 'l10n_gcc_invoice',
                'base_report_header',
                'account_move_line_images',  # due to product_image field in account.move.line
                'product_name_ar',
#'invoice_bank_information'
],

    'data': [
        'report/layout.xml',
        'report/qrcode.xml',
        'report/document.xml',
        'report/report.xml',
        'views/account_move.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
