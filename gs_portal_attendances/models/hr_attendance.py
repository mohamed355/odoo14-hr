# -*- coding: utf-8 -*-
""" init object """
import math
from odoo import fields, models, api


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
            # 'url': 'http://maps.google.com/maps?q=%s,%s' % (lat, long),
            'url': 'https://www.mapdevelopers.com/what-is-my-address.php?lat=%s&lng=%s' % (lat, long),
            'target': 'new'
        }

    def action_open_check_in_location(self):
        return self.action_open_location(self.check_in_latitude, self.check_in_longitude)

    def action_open_check_out_location(self):
        return self.action_open_location(self.check_out_latitude, self.check_out_longitude)

    @api.model
    def calculate_dist_to_company(self, x, y):
        R = 6371008.7714
        lat1 = math.radians(x[0])
        lon1 = math.radians(x[1])
        lat2 = math.radians(y[0])
        lon2 = math.radians(y[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance




