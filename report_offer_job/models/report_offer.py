from odoo import api, fields, models, tools


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def action_send_offer(self):
        print('Send Email')
        # self.env['report.job.offer'].create({
        #     'name':self.partner_name,
        #         'hiring':self.hiring_ids[0].name,
        #         'job_title':self.hiring_ids[0].job_id.name,
        #         'location':self.hiring_ids[0].location,
        #         'client':self.hiring_ids[0].client.name,
        #         'offer_job_title':self.offer_job_id,
        #         'offer_date':fields.Datetime.now(),
        #         'package_salary':self.package_salary,
        #         'housing':self.housing,
        #         'basic':self.basic,
        #         'transportation':self.transportation,
        # })
        template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
        template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
        template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
        template = None
        if self.template == 'ksa':
            template = self.env['mail.template'].browse(template_ksa.id)
        if self.template == 'egy':
            template = self.env['mail.template'].browse(template_egy.id)
        if self.template == 'saudi':
            template = self.env['mail.template'].browse(template_sa.id)

        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            # 'proforma': sale.env.context.get('proforma', False),
            'force_email': True,
            # 'model_description': sale.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


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
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )
    offer_state = fields.Selection(string="Offer State", selection=[('to', 'To Be Offered'), ('offered', 'Offered'),('offeracc', 'Offer Accepted'),('offerdi', 'Offer Declined') ], required=False, )
    decline_state = fields.Selection(string="Decline Reason", selection=[('salary', 'Salary'), ('retain', 'Retain'),('another', 'Another Offer'),('no', 'No Show'),('other', 'Other') ], required=False, )
    joining_date = fields.Date(string="Joining Date", required=False, )
    comments = fields.Char(string="Comments", required=False, )