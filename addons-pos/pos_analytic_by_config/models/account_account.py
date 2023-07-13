from odoo import api, models

class AccountAccount(models.Model):
    _inherit = "account.account"

    def _check_account_pnl(self):
        """
            Checks if account is under profit and loss, so AA can be added to its JE
        """
        return self.mapped('user_type_id.internal_group') in [['income'], ['expense']] and True or False
