# -*- coding: utf-8 -*-
from odoo import models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _set_view_context(self):
        self = self.with_context(search_default_locationgroup=True)
        return super(StockQuant, self)._set_view_context()