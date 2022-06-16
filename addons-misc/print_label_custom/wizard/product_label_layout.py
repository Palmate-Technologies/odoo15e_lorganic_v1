# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    def _prepare_report_data(self):
        if self.custom_quantity <= 0:
            raise UserError(_('You need to set a positive quantity.'))

        # Get layout grid
        if self.print_format == 'dymo':
            xml_id = 'product.report_product_template_label_dymo'
        elif 'x' in self.print_format:
            xml_id = 'product.report_product_template_label'
        else:
            xml_id = ''

        active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'

        ctx = self._context
        exp_dates = {}
        if ctx.get('active_model','False') == 'stock.picking' and ctx.get('active_id'):
            picking = self.env[ctx.get('active_model','stock.picking')].browse(ctx.get('active_id'))
            for product_id in products:
                for move in picking.move_ids_without_package.filtered(lambda m:m.product_id.id==product_id):
                    added=False
                    for move_line in move.move_line_nosuggest_ids:
                        added=True
                        exp_dates[move_line.product_id.id] = move_line.expiration_date.date()
                    if not added:
                        exp_dates[move.product_id.id] = ''

        if ctx.get('active_model', 'False') == 'product.template' and ctx.get('active_id'):
            template = self.env[ctx.get('active_model', 'product.template')].browse(ctx.get('active_id'))
            new_products = template.product_variant_ids
            lots = self.env['stock.production.lot'].search([('product_id','in',new_products.ids)],order='id desc')
            if lots:
                exp_dates[new_products[0].id] = lots[0].expiration_date.date()
            else:
                exp_dates[new_products[0].id] = ''

        if ctx.get('active_model', 'False') == 'product.product' and ctx.get('active_id'):
            new_product = self.env[ctx.get('active_model', 'product.product')].browse(ctx.get('active_id'))
            lots = self.env['stock.production.lot'].search([('product_id','=',new_product.id)],order='id desc')
            if lots:
                exp_dates[new_product.id] = lots[0].expiration_date.date()
            else:
                exp_dates[new_product.id] = ''

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
            'exp_dates':exp_dates,
        }
        return xml_id, data
