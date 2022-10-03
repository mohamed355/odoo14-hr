from odoo import api, fields, models, Command
from collections import defaultdict
from datetime import date, datetime


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    date_deadline = fields.Date('Due Date', index=True, required=True,)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )
    lead_id = fields.Many2one(comodel_name="crm.lead", string="Leads", required=False, )
    date_from = fields.Datetime(string="Date From", required=False, )
    date_to = fields.Datetime(string="Date To", required=False, )
    crm_user_ids = fields.Many2many(comodel_name="res.users", relation="resuseerscrm", column1="rescrm",
                                    column2="userescrm",
                                    string="Users", compute="_compute_users_crm")

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        if self.activity_type_id:
            if self.activity_type_id.summary:
                self.summary = self.activity_type_id.summary
            # self.date_deadline = self._calculate_date_deadline(self.activity_type_id)
            self.user_id = self.activity_type_id.default_user_id or self.env.user
            if self.activity_type_id.default_note:
                self.note = self.activity_type_id.default_note


    @api.depends('activity_type_id')
    def _compute_users_crm(self):
        for record in self:
            users = self.env.ref('sales_team.group_sale_manager').users.ids
            record.crm_user_ids = users

    @api.model
    def create(self, values):
        res = super(MailActivity, self).create(values)
        for record in res:
            record.date_deadline = datetime.strftime(record.date_from, '%Y-%m-%d')
        return res

    @api.onchange('partner_id', 'opportunity_id', 'lead_id')
    def onchange_fields_filter(self):
        if self.partner_id:
            self.res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1).id
            self.res_id = self.partner_id.id
        if self.opportunity_id:
            self.res_model_id = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1).id
            self.res_id = self.opportunity_id.id
        if self.lead_id:
            self.res_model_id = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1).id
            self.res_id = self.lead_id.id
