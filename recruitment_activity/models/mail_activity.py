from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'


    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Request Code", required=False, )
    app_id = fields.Many2one(comodel_name="hr.applicant", string="Application Code", required=False, )

    @api.onchange('hiring_id','app_id')
    def onchange_hiring_id_filter(self):
        if self.hiring_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','hiring.request')],limit=1).id
            self.res_id = self.hiring_id.id
        if self.app_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','hr.applicant')],limit=1).id
            self.res_id = self.app_id.id


