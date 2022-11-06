from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_in = fields.Selection(string="Leave In", selection=[('egypt', 'Egypt'), ('o_of_egy', 'Out Of Egypt'), ],
                                required=False, )
