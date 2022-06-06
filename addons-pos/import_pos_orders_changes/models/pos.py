# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    name = fields.Char(string='Order Ref', required=True, readonly=False, copy=False, default='/')
    date_order = fields.Datetime(string='Date', readonly=False, index=True, default=fields.Datetime.now)
    amount_tax = fields.Float(string='Taxes', digits=0, readonly=False, required=True)
    amount_total = fields.Float(string='Total', digits=0, readonly=False, required=True)
    amount_paid = fields.Float(string='Paid', states={'draft': [('readonly', False)]},
                               readonly=False, digits=0, required=True)
    amount_return = fields.Float(string='Returned', digits=0, required=True, readonly=False)
    payment_ids = fields.One2many('pos.payment', 'pos_order_id', string='Payments', readonly=False)


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    price_subtotal = fields.Float(string='Subtotal w/o Tax', digits=0,
                                  readonly=False, required=True)
    price_subtotal_incl = fields.Float(string='Subtotal', digits=0,
                                       readonly=False, required=True)
    tax_ids = fields.Many2many('account.tax', string='Taxes', readonly=False)


class PosPayment(models.Model):
    _inherit = "pos.payment"

    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id', readonly=False,
                             help="Total amount of the payment.")


class PosSession(models.Model):
    _inherit = 'pos.session'

    name = fields.Char(string='Session ID', required=True, readonly=False, default='/')
    start_at = fields.Datetime(string='Opening Date', readonly=False)
    stop_at = fields.Datetime(string='Closing Date', readonly=False, copy=False)
