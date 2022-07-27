from odoo import api, fields, models, Command
from collections import defaultdict
from  datetime import date,datetime

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )
    lead_id = fields.Many2one(comodel_name="crm.lead", string="Leads", required=False, )
    date_from = fields.Datetime(string="Date From", required=True,default=datetime.today().strftime('%Y-%m-%d 02:00:00'))
    date_to = fields.Datetime(string="Date To", required=True, default=datetime.today().strftime('%Y-%m-%d 09:00:00'))

    @api.onchange('partner_id','opportunity_id','lead_id')
    def onchange_fields_filter(self):
        if self.partner_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','res.partner')],limit=1).id
            self.res_id = self.partner_id.id
        if self.opportunity_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id
            self.res_id = self.opportunity_id.id
        if self.lead_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id
            self.res_id = self.lead_id.id






