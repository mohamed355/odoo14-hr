from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'


    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", required=False, )

    @api.onchange('hiring_id')
    def onchange_hiring_id_filter(self):
        if self.hiring_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','hiring.request')],limit=1).id
            self.res_id = self.hiring_id.id


