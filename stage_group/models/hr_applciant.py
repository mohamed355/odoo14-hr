from odoo import api, fields, models 
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.constrains('stage_id')
    def _constrains_stage_id_ah(self):
        for x in self:
            print("adsd", x.stage_id.name)
            if x.stage_id.name in ["Hold", "Completed"]:
                x.stage_id = None
                x.hiring_ids = None
                hiring_ids = self.env['hiring.request'].search([('application_ids', 'in', x.id)])
                print(hiring_ids)
                for h in hiring_ids:
                    h.update({'application_ids': [(3, x.id, False)]})
            if x.stage_id.name == "Offer Accepted":
                x.acc_date = fields.Date.today()
            if x.env.uid in x.stage_id.user_ids.ids:
                print("Access")
            else:
                raise ValidationError("You Need To Access To Move In This Stage")