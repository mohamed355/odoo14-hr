from odoo import models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def change_attandance_by_user(self):
        action_message = {}
        if self.user_id:
            modified_attendance = self.with_user(self.user_id).sudo()._attendance_action_change()
        else:
            modified_attendance = self.sudo()._attendance_action_change()
        action_message['attendance'] = modified_attendance.sudo().read()[0]
        return action_message