from odoo import api, fields, models, tools


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def action_send_offer(self):
        print('Send Email')
        self.env['report.job.offer'].create({
            'name':self.partner_name,
                'hiring':self.hiring_ids[0].name,
                'job_title':self.hiring_ids[0].job_id.name,
                'location':self.hiring_ids[0].location,
                'client':self.hiring_ids[0].client.name,
                'offer_job_title':self.offer_job_id,
                'offer_date':fields.Datetime.now(),
                'package_salary':self.package_salary,
                'housing':self.housing,
                'basic':self.basic,
                'transportation':self.transportation,
        })
        template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
        template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
        template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
        if self.template == 'ksa':
            self.env['mail.template'].browse(template_ksa.id).send_mail(self.id, force_send=True)
        if self.template == 'egy':
            self.env['mail.template'].browse(template_egy.id).send_mail(self.id, force_send=True)
        if self.template == 'saudi':
            self.env['mail.template'].browse(template_sa.id).send_mail(self.id, force_send=True)




class ReportJobOffer(models.Model):
    _name = 'report.job.offer'

    name = fields.Char(string="Name", required=False, )
    hiring = fields.Char(string="Hiring", required=False)
    job_title = fields.Char(string="Job Title", required=False)
    offer_job_title = fields.Char(string="Job Title", required=False)
    location = fields.Char(string="Location", required=False)
    client = fields.Char(string="Client", required=False)
    offer_date = fields.Datetime(string="Offer Date", required=False, )
    package_salary = fields.Integer(string="Package", required=False, )
    housing = fields.Integer(string="Housing", required=False,)
    basic = fields.Integer(string="Basic", required=False,)
    transportation = fields.Integer(string="Transportation", required=False,)
