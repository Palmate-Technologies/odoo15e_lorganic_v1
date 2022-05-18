
from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_image = fields.Binary(string="Image", related="product_id.image_1920")


