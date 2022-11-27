from odoo import api, fields, models


class ExpirationConf(models.Model):
    _name = 'expire.conf'

    name = fields.Char()
    days = fields.Integer(string="Days", )
    mail = fields.Boolean(string="Email", )
    activity = fields.Boolean(string="Activity", )
    users_ids = fields.Many2many(comodel_name="res.users",
                                 string="Users", )
