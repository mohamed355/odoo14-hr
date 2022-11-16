from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_leave_in_id = fields.Many2one(comodel_name="hr.leave.in", string="Live", required=False, )
    dir = fields.Selection(string="Direction", selection=[('in', 'Internal'), ('ex', 'External'), ], required=False, )

