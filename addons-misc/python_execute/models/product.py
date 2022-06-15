# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Template(models.Model):
    _inherit = 'product.template'

    def write_custom(self, vals):
        print("write custom called")
        """
        Custom method to call from xmlrpc call.
        """
        self.write(vals)
        return True