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
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    image_header_file = fields.Binary(string="Report Header")
    image_footer_file = fields.Binary(string="Report Footer")


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    image_header_file = fields.Binary(related="company_id.image_header_file")
    image_footer_file = fields.Binary(related="company_id.image_footer_file")


