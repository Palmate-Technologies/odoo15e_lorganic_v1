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


class PythonExecuteWizard(models.TransientModel):
    _name = "python.execute.wizard"
    _description = "Python Execute Wizard"

    file = fields.Binary(string="Script", required=True)
    result = fields.Text()
    pin = fields.Char(string="PIN")

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






