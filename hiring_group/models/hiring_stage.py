from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class HiringStage(models.Model):
    _inherit = 'hiring.stage'

    user_ids = fields.Many2many(comodel_name="res.users", relation="rsesussers", column1="srfses", column2="usassders",
                                string="Users", )



