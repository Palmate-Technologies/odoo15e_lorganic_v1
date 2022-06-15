from odoo import api, fields, models


class PrintLabelWizard(models.Model):
    _name = "print.label.wizard"

    # pharmacy_name = fields.Char(string="Pharmacy")
    tel = fields.Char(string="Tel")
    patient_name = fields.Char(string="Patient")
    product_id = fields.Many2one("product.product", string="Medicine")
    dose = fields.Many2one('dose.dose', string='Dose')
    expiry_date = fields.Date(string="Expiry Date")
    batch = fields.Char(string="Batch")
    pharmacist = fields.Many2one('res.users', string="Pharmacist")

    def print_label(self):
        return self.env.ref('print_label_custom.action_report_print_label_wizard').report_action(self)

    @api.onchange('product_id')
    def onchange_product_id(self):
        product = self.product_id
        lots = self.env['stock.production.lot'].search([('product_id', '=', product.id)], order='id desc')
        if lots:
            self.expiry_date = lots[0].expiration_date
        else:
            self.expiry_date = ''
        lot_name = self.env['stock.production.lot'].search([('product_id', '=', product.id)], order='id desc')
        if lot_name:
            self.batch = lot_name[0].name
        else:
            self.batch = ''
