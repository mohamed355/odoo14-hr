from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class HiringRequest(models.Model):
    _inherit = 'hiring.request'

    @api.constrains('stage_id')
    def _constrains_stage_id_hirings(self):
        for x in self:
            print("adsd", x.stage_id.name)
            print(self.env.user.id, 'in', x.stage_id.user_ids.ids)
            if x.stage_id.name != False:
                if self.env.user.id in x.stage_id.user_ids.ids:
                    print("Access")
                else:
                    raise ValidationError("You Need To Access To Move In This Stage")
