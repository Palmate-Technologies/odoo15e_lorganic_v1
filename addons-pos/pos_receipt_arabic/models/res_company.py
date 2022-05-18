from odoo import api, fields, models, _


class Company(models.Model):
    _inherit = "res.company"
    
    arabic_name = fields.Char(compute='_compute_arabic_name', string='Arabic Name')
    
    def _compute_arabic_name(self):
        for company in self:
            company.arabic_name = company.with_context({'lang': 'ar_001'}).partner_id.name or ''
            # company.arabic_name = "اسم الاختبار"  # Fixme
