from odoo import api, fields, models
from datetime import timedelta


class AssignUsers(models.TransientModel):
    _inherit = 'assign.users'

    def assign_users(self):
        hiring = self.env['hiring.request'].browse(self.env.context.get('active_id'))
        hiring.approved = True
        hiring.acc_date = fields.Date.today()
        for user in self.user_ids:
            hiring.update({'user_ids_real': [(4, user.id)]})
            self.env['user.history'].create({
                'user_id': user.id,
                'start_date': fields.Datetime.today(),
                'hiring_id': hiring.id,
            })
            self.env['mail.activity'].create({
                'activity_type_id': self.env['mail.activity.type'].search([('name', '=', 'Sourcing')], limit=1).id,
                'user_id': user.id,
                'res_id': hiring.id,
                'date_deadline': fields.Date.today() + timedelta(days=2),
                'res_model_id': self.env['ir.model'].sudo().search(
                    [('model', '=', 'hiring.request')], limit=1).id,
            })
