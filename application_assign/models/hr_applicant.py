from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def open_create_wizard(self):
        print("ezz")


