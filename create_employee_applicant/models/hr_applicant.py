from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def create_employee_from_applicant(self):
        return {
            'name': 'Live In',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.leave.in',
            'target': 'new'
        }


class HrLeave(models.Model):
    _name = 'hr.leave.in'

    leave_in = fields.Selection(string="Live In", selection=[('egypt', 'Egypt'), ('o_of_egy', 'Out Of Egypt'), ],
                                required=False, )

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
                    'default_name': applicant.partner_name or contact_name,
                    'default_job_id': applicant.job_id.id,
                    'default_job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'default_department_id': applicant.department_id.id or False,
                    'default_address_id': applicant.company_id and applicant.company_id.partner_id
                                          and applicant.company_id.partner_id.id or False,
                    'default_work_email': applicant.department_id and applicant.department_id.company_id
                                          and applicant.department_id.company_id.email or False,
                    'default_work_phone': applicant.department_id.company_id.phone,
                    'form_view_initial_mode': 'edit',
                    'default_applicant_id': applicant.ids,
                    'default_leave_in': self.leave_in,
                }
        dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
        dict_act_window['context'] = employee_data
        return dict_act_window


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
