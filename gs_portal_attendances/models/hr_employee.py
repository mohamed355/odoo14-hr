from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    allow_attendance_check = fields.Boolean(string="Allow Attendance Any Location", default=False  )


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def change_attandance_by_user(self):
        action_message = {}
        if self.user_id:
            modified_attendance = self.with_user(self.user_id).sudo()._attendance_action_change()
        else:
            modified_attendance = self.sudo()._attendance_action_change()
        if 'error' in modified_attendance:
            return modified_attendance
        action_message['attendance'] = modified_attendance.sudo().read()[0]
        return action_message

    def _attendance_action_change(self):
        context = dict(self._context)
        if not self.allow_attendance_check and 'location' in context:
            lat = context['location']['latitude']
            long = context['location']['longitude']
            check_cord = (lat, long)
            comp_cord = (self.env.company.latitude, self.env.company.longitude)
            dist = self.env['hr.attendance'].calculate_dist_to_company(check_cord, comp_cord)
            if abs(dist) > self.env.company.allowed_attendance_distance:
                return {
                    'error': "Please Check From The Company Correct Location"
                }

        if 'location' in context:
            if self.attendance_state != 'checked_in':
                context['default_check_in_latitude'] = context['location']['latitude']
                context['default_check_in_longitude'] = context['location']['longitude']
                return super(HrEmployee, self.with_context(context))._attendance_action_change()
            else:
                attendance = super(HrEmployee, self)._attendance_action_change()
                attendance.check_out_latitude = context['location']['latitude']
                attendance.check_out_longitude = context['location']['longitude']
                return attendance

        else:
            return super(HrEmployee, self)._attendance_action_change()