from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    user_ids = fields.Many2many(comodel_name="res.users", relation="resussers", column1="sres", column2="usasders",
                                string="Users", )



