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
import base64
import textwrap
from datetime import datetime
from odoo import models, fields
from odoo.exceptions import UserError
import xmlrpc.client
import logging
_logger = logging.getLogger(__name__)


class PythonExecuteWizard(models.TransientModel):
    _name = "python.execute.wizard"
    _description = "Python Execute Wizard"

    file = fields.Binary(string="Script", required=True)
    result = fields.Text()
    pin = fields.Char(string="PIN")

    def _get_database_connection(self):

        _logger.info("_get_database_connection called")
        url1 = "https://lorganic.odoo.com"
        db1 = "peninsu-lorganic-master-295199"
        u1 = "kaleem@l-organic.com"
        p1 = "Kaleem123"
        common1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url1))
        models1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url1), allow_none=True)
        v1 = common1.version()
        print("V12",v1)
        _logger.info("V12 %s",v1)

        # Local 15
        # url2 = "http://localhost:8015"
        # db2 = "LORGANIC-JUNE11"
        url2 = "https://palmate-technologies-lorganic15.odoo.com"
        db2 = "palmate-technologies-odoo15e-lorganic-v1-master-4932728"
        u2 = "admin"
        p2 = "admin123"
        common2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url2))
        models2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url2), allow_none=True)
        v2 = common2.version()
        _logger.info("V15 %s", v2)

        uid1 = common1.authenticate(db1, u1, p1, {})
        uid2 = common2.authenticate(db2, u2, p2, {})
        db12 = {
            'url1': url1,
            'db1': db1,
            'u1': u1,
            'p1': p1,
            'common1':common1,
            'models1':models1,
            'v1':v1,
            'uid1':uid1,
        }
        db15 = {
            'url2': url2,
            'db2': db2,
            'u2': u2,
            'p2': p2,
            'common2':common2,
            'models2':models2,
            'v2':v2,
            'uid2':uid2,
        }
        return db12, db15

    def migrate_product_images(self):
        db12, db15 = self._get_database_connection()
        db1 = db12.get('db1')
        uid1 = db12.get('uid1')
        p1 = db12.get('p1')
        models1 = db12.get('models1')

        db2 = db15.get('db2')
        uid2 = db15.get('uid2')
        p2 = db15.get('p2')
        models2 = db15.get('models2')

        # db1_product_ids = models1.execute_kw(db1, uid1, p1, 'product.template', 'search', [[('barcode','=','8009123745972')]])
        db1_product_ids = models1.execute_kw(db1, uid1, p1, 'product.template', 'search', [[]])
        for db1_product_id in db1_product_ids:
            product = models1.execute_kw(db1, uid1, p1, 'product.template', 'read', [db1_product_id], {'fields': ['barcode','image_medium']})
            product = product[0]

            # image_variant_1920
            db2_product_ids = models2.execute_kw(db2, uid2, p2, 'product.template', 'search',
                                                 [[('barcode', '=', product.get('barcode'))]])
            if not len(db2_product_ids):
                continue
            db2_product_id = db2_product_ids[0]
            write_vals = {
                'image_1920':product.get('image_medium','')
            }
            models2.execute_kw(db2, uid2, p2, 'product.template', 'write_custom', [[db2_product_id], (write_vals)])
            _logger.info("Image uploaded")

        _logger.info("Image upload finished.")
        return True


    def check_access(self):
        self.ensure_one()
        if self.pin != str(datetime.now().year + datetime.now().month + datetime.now().day):
            raise UserError("Invalid PIN")

    def button_execute(self):
        self.ensure_one()
        self.check_access()
        self.result = False
        content = base64.b64decode(self.file).decode()
        prefix = 'def execute(self):'

        if not content.startswith(prefix):
            raise Warning('Invalid')

        content = content.replace(prefix, "")

        def print(text):
            self.result = str(self.result or "") + str(text) + '\n'

        exec(textwrap.dedent(content))






