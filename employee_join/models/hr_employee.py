from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection(string="State", selection=[('new', 'New'), ('joined', 'Joined'), ], required=False,
                             default='new')
    joined = fields.Boolean(string="Joined", )

    def join(self):
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

    def emp_conf(self):
        emp_objs = self.env['emp.act'].search([])
        for emp in emp_objs:
            activity_obj = self.env['mail.activity'].create({
                'activity_type_id': emp.activity_type_id.id,
                # 'summary': emp.description,
                'date_deadline': fields.Date.today(),
                'user_id': emp.user_id.id,
                'note': emp.description,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                'res_id': self.id
            })
        self.state = 'joined'
