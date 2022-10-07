from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def check_group_every(self):
        if self.env.user.has_group("everybody_calendar_hide.everybody_show"):
            return True
        else:
            return False
