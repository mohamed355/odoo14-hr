from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_in = fields.Selection(string="Leave In", selection=[('egypt', 'Egypt'), ('o_of_egy', 'Out Of Egypt'), ],
                                required=False, )

    @api.model
    def create(self, values):
        # Add code here
        res = super(HrEmployee, self).create(values)
        for record in res:
            if record.applicant_id:
                if record.leave_in == 'egypt':
                    print('eg')
                    temp = self.env['mail.template'].search([('name', '=', 'Send To Egypt')])
                    print(temp.email_to)
                    temp.sudo().send_mail(record.applicant_id.id, force_send=True)
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': "New Employee",
                        'user_id': self.env['res.users'].search([('id', '=', 42)]).id,
                        'note': "New Employee",
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                        'res_id': record.id
                    })
                if self.leave_in == 'o_of_egy':
                    template = self.env.ref('create_employee_applicant.o_egypt_email_template')
                    template.sudo().send_mail(record.applicant_id.id, force_send=True)
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': "New Employee",
                        'user_id': self.env['res.users'].search([('id', '=', 37)]).id,
                        'note': "New Employee",
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                        'res_id': record.id
                    })
        return res
