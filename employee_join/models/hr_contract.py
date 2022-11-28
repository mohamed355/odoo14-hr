from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # @api.model
    # def create(self, values):
    #     if values['employee_id']:
    #         emp = self.env['hr.employee'].search([('id', '=', values['employee_id'])])
    #         if not emp.joined:
    #             raise ValidationError("Employee Must Joined")
    #     return super(HrContract, self).create(values)
