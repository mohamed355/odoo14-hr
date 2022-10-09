from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joined = fields.Boolean(string="Joined", )

    def join(self):
        self.joined = True
        return {
            'name': 'Employee Join',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.join',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': self.id,
            },
            'target': 'new'

        }
