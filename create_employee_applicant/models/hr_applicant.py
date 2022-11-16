from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def create_employee_from_applicant(self):
        if self.hiring_ids:
            return {
                'name': 'Live In',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hr.leave.in',
                'context': {
                    'default_location': self.location,
                    'default_nationality_id': self.nationality_id.id,
                    'default_dir': self.hiring_ids[0].dir,
                },
                'target': 'new'
            }
        else:
            return {
                'name': 'Live In',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hr.leave.in',
                'context': {
                    'default_location': self.location,
                    'default_nationality_id': self.nationality_id.id,
                },
                'target': 'new'
            }


class HrLeave(models.Model):
    _name = 'hr.leave.in'

    location = fields.Selection(string="Location", selection=[('off', 'Offshore'), ('on', 'Onsite'), ],
                                required=False, readonly=True)
    nationality_id = fields.Many2one(comodel_name="nationality", string="Nationality", required=False, )
    assign_to = fields.Selection(string="Assign To", selection=[('eg', 'Egypt HR Office'), ('sr', 'Saudi HR Office'), ],
                                 required=False, )
    note = fields.Text(string="Note", required=False, )
    dir = fields.Selection(string="Direction", selection=[('in', 'Internal'), ('ex', 'External'), ], required=False, )

    def go_to_employee(self):
        employee = False
        applicants = self.env['hr.applicant'].browse(self.env.context.get('active_id'))
        for applicant in applicants:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                applicant.partner_id = new_partner_id
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee_data = {
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                                  and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id.company_id.phone,
                    'applicant_id': applicant.ids,
                    'hr_leave_in_id': self.id,
                    'location': self.location,
                    'assign_to': self.assign_to,
                    'note': self.note,
                    'dir': self.dir,
                }
                emp_obj = self.env['hr.employee'].sudo().create(employee_data)
                if self.assign_to == 'eg':
                    print('eg')
                    temp = self.env['mail.template'].search([('name', '=', 'Send To Egypt')])
                    print(temp.email_to)
                    temp.sudo().send_mail(applicant.id, force_send=True)
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': "New Employee",
                        'user_id': self.env['res.users'].search([('id', '=', 2)]).id,
                        'note': "New Employee",
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                        'res_id': emp_obj.id
                    })
                if self.assign_to == 'sr':
                    template = self.env.ref('create_employee_applicant.o_egypt_email_template')
                    template.sudo().send_mail(applicant.id, force_send=True)
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': "New Employee",
                        'user_id': self.env['res.users'].search([('id', '=', 2)]).id,
                        'note': "New Employee",
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                        'res_id': emp_obj.id
                    })
                if self.dir == 'in':
                    emp_objs = self.env['emp.act'].search([('internal', '=',True)])
                    for emps in emp_objs:
                        activity_obj = self.env['mail.activity'].create({
                            'activity_type_id': emps.activity_type_id.id,
                            # 'summary': emp.description,
                            'date_deadline': fields.Date.today(),
                            'user_id': emps.user_id.id,
                            'note': emps.description,
                            'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                            'res_id': emp_obj.id
                        })


class EmployeeEmailConf(models.Model):
    _name = 'emp.email.conf'

    leave_in = fields.Selection(string="Live In", selection=[('egypt', 'Egypt'), ('o_of_egy', 'Out Of Egypt'), ],
                                required=False, )
    template_id = fields.Many2one('mail.template', 'Template')
    email = fields.Char(string="Email", required=False, )
    show_change = fields.Boolean(string="Show Change", )

    @api.onchange('email')
    def _onchange_email(self):
        self.show_change = True

    def change_email(self):
        self.template_id.email_to = 'i.osama@rawafdtech.net'
        self.template_id.email_to = self.email
        self.show_change = False
