from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_email = fields.Char('Work Email', required=False, )
    state = fields.Selection(string="State", selection=[('new', 'New'), ('joined', 'Joined'), ], required=False,
                             default='new')
    joined = fields.Boolean(string="Joined", )
    location = fields.Selection(string="Location", selection=[('off', 'Offshore'), ('on', 'Onsite'), ],
                                required=False, readonly=True)
    nationality_id = fields.Many2one(comodel_name="nationality", string="Nationality", required=False, )
    assign_to = fields.Selection(string="Assign To", selection=[('eg', 'Egypt HR Office'), ('sr', 'Saudi HR Office'), ],
                                 required=False, )
    note = fields.Text(string="Note", required=False, )
    dir = fields.Selection(string="Direction", selection=[('in', 'Internal'), ('ex', 'External'), ], required=False, )

    def join(self):
        return {
            'name': 'Employee Join',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.join',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': self.id,
                'default_hr_leave_in_id': self.hr_leave_in_id.id,
                'default_location': self.hr_leave_in_id.location,
                'default_assign_to': self.hr_leave_in_id.assign_to,
                'default_note': self.hr_leave_in_id.note,
                'default_dir': self.hr_leave_in_id.dir,
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
