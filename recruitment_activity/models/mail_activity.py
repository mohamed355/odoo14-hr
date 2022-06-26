from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    application_id = fields.Many2one(comodel_name="hr.applicant", string="Application", required=False, )

    @api.onchange('application_id')
    def onchange_application_id_filter(self):
        if self.application_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','hr.applicant')],limit=1).id
            self.res_id = self.application_id.id


