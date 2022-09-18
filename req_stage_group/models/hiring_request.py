from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class HrApplicant(models.Model):
    _inherit = 'hiring.request'

    @api.constrains('stage_id')
    def _constrains_stage_id(self):
        for x in self:
            if self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager') or self.env.user.has_group(
                    'hr_recruitment.group_hr_recruitment_man'):
                print("Access")
            else:
                raise ValidationError("You Need To Access To Move In This Stage")
