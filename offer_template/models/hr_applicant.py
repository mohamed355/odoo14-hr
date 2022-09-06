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


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def default_template_id(self):
        default = None
        print(self.model)
        if self.model == 'hr.applicant':
            template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
            template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
            template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
            app = self.env['hr.applicant'].browse(self.res_id)
            if app.template == 'ksa':
                default = template_ksa.id
            if app.template == 'egy':
                default = template_egy.id
            if app.template == 'saudi':
                default = template_sa.id
            print(default)
        return default
    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('model', '=', model)]",default = default_template_id)