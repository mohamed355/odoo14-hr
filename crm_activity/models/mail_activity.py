from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )

    @api.onchange('partner_id','opportunity_id')
    def onchange_fields_filter(self):
        if self.partner_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','res.partner')],limit=1).id
            self.res_id = self.partner_id.id
        if self.opportunity_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id
            self.res_id = self.opportunity_id.id

