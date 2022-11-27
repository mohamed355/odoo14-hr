from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def action_cron_auto_emp_expire(self):
        """ Perform the automatic transfer for the all active move models. """
        emp_objs = self.search([])
        for emp in emp_objs:
            act = self.env['expire.conf'].search([('activity', '=', True)])
            email = self.env['expire.conf'].search([('mail', '=', True)])
            if act:
                if emp.visa_expire:
                    print(abs(fields.Date.today() - emp.visa_expire).days)
                    if abs(fields.Date.today() - emp.visa_expire).days == act.days:
                        for user in act.users_ids:
                            self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'summary': "%s days left for the visa to expire For %s" % (act.days, emp.name),
                                'user_id': user.id,
                                'note': "",
                                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                                'res_id': emp.id
                            })
                if emp.work_permit_expiration_date:
                    if abs(fields.Date.today() - emp.work_permit_expiration_date) == act.days:
                        for user in act.users_ids:
                            self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'summary': "%s days left for the Work Permit to expire For %s" % (act.days, emp.name),
                                'user_id': user.id,
                                'note': "",
                                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                                'res_id': emp.id
                            })
                if emp.acc_date:
                    if abs(fields.Date.today() - emp.acc_date) == act.days:
                        for user in act.users_ids:
                            self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'summary': "%s days left for the Accommodation to expire For %s" % (act.days, emp.name),
                                'user_id': user.id,
                                'note': "",
                                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                                'res_id': emp.id
                            })
            if email:
                if emp.visa_expire:
                    print(abs(fields.Date.today() - emp.visa_expire).days, "EMAIIIL")
                    print(email.days, "EMAIIIL")
                    if abs(fields.Date.today() - emp.visa_expire).days == email.days:
                        for user in email.users_ids:
                            composer = self.env['mail.compose.message'].create({
                                'subject': 'Expire Visa',
                                'partner_ids': [(4, user.partner_id.id)],
                                'res_id': emp.id,
                                'model': 'hr.employee',
                                'body': "",
                                'composition_mode': 'comment',
                            })
                            update_values = \
                                composer._onchange_template_id(False, 'comment', 'hr.employee', emp.id)[
                                    'value']
                            composer.write(update_values)
                            composer._action_send_mail()
                            print(composer.partner_ids)
                            print(composer)



                # if emp.work_permit_expiration_date:
                #     if abs(fields.Date.today() - emp.work_permit_expiration_date) == email.days:
                #         for user in email.users_ids:
                #             self.env['mail.activity'].create({
                #                 'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                #                 'summary': "%s days left for the visa to expire For %s" % (email.days, emp.name),
                #                 'user_id': user.id,
                #                 'note': "",
                #                 'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                #                 'res_id': emp.id
                #             })
                # if emp.acc_date:
                #     if abs(fields.Date.today() - emp.acc_date) == email.days:
                #         for user in email.users_ids:
                #             self.env['mail.activity'].create({
                #                 'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                #                 'summary': "%s days left for the visa to expire For %s" % (email.days, emp.name),
                #                 'user_id': user.id,
                #                 'note': "",
                #                 'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')]).id,
                #                 'res_id': emp.id
                #             })
