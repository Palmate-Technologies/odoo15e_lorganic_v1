from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id,
                                       credit_account_id, description):
        rslt = super()._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id,
                                       credit_account_id, description)

        pos_config = False
        if self.picking_id.pos_session_id:
            pos_config = self.picking_id.pos_session_id.config_id
        elif self.picking_id.pos_order_id:
            pos_config = self.picking_id.pos_order_id.session_id.config_id

        if pos_config:
            ### Update AA
            Account = self.env['account.account']
            credit_account = Account.browse(rslt['credit_line_vals']['account_id'])
            debit_account = Account.browse(rslt['debit_line_vals']['account_id'])
            product_accounts = self.product_id.product_tmpl_id._get_product_accounts()

            if credit_account not in (product_accounts['stock_input'], product_accounts['stock_output'], product_accounts['stock_valuation']):
                rslt['credit_line_vals']['analytic_account_id'] = pos_config.account_analytic_id.id
            if debit_account not in (product_accounts['stock_input'], product_accounts['stock_output'], product_accounts['stock_valuation']):
                rslt['debit_line_vals']['analytic_account_id'] = pos_config.account_analytic_id.id
        return rslt
