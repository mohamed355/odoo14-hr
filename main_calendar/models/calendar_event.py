from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    technical = fields.Boolean(string="Technical", )
