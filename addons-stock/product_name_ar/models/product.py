# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Template(models.Model):
    _inherit = 'product.template'
    
    name_arabic = fields.Char(string="Product Arabic Name")