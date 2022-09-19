from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    @api.model
    def check_access(self):
        usr = self.env.user
        if usr.has_group('import_access.import_group'):
            return False
        else:
            return True
