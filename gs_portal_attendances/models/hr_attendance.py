# -*- coding: utf-8 -*-
""" init object """
from odoo import fields, models, api, _ ,tools, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime , date ,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime as fieldsDatetime
import calendar
from odoo import http
from odoo.http import request
from odoo import tools

import logging

LOGGER = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    check_in_latitude = fields.Float()
    check_in_longitude = fields.Float()
    check_out_latitude = fields.Float()
    check_out_longitude = fields.Float()

    def action_open_location(self, lat, long):
        return {
            'type': 'ir.actions.act_url',
            'name': 'Check In Location',
            'url': 'http://maps.google.com/maps?q=%s,%s' % (lat, long),
            'target': 'new'
        }

    def action_open_check_in_location(self):
        return self.action_open_location(self.check_in_latitude, self.check_in_longitude)

    def action_open_check_out_location(self):
        return self.action_open_location(self.check_out_latitude, self.check_out_longitude)




