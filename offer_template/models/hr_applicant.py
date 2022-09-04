from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def action_send_offer(self):
        print('Send Email')
        template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
        template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
        template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
        if self.template == 'ksa':
            self.env['mail.template'].browse(template_ksa.id).send_mail(self.id, force_send=True)
        if self.template == 'egy':
            self.env['mail.template'].browse(template_egy.id).send_mail(self.id, force_send=True)
        if self.template == 'saudi':
            self.env['mail.template'].browse(template_sa.id).send_mail(self.id, force_send=True)


