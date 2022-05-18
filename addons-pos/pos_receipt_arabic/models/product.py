from odoo import fields, models, api


class Product(models.Model):
    _inherit = "product.product"

    arabic_name = fields.Char(compute='_compute_arabic_name')
    english_name = fields.Char(compute='_compute_arabic_name')

    def _compute_arabic_name(self):
        for product in self:
            product.english_name = product.with_context({'lang': 'en_US'}).name or ''
#            product.arabic_name = product.with_context({'lang': 'ar_001'}).name or ''
            product.arabic_name = product.name_arabic
 #           if product.english_name == product.arabic_name:
  #              product.arabic_name = ''
