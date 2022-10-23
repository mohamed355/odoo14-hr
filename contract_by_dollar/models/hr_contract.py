from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    currency_wage_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )
    wage_convert = fields.Float(string="Wage With Currency", required=False, )
    wage_1 = fields.Monetary(string="Wage 1", required=False, )
    currency_wage_1_id = fields.Many2one(comodel_name="res.currency", string="Currency 1", required=False, )
    wage_1_convert = fields.Float(string="Wage 1 With Currency", required=False, )

    @api.onchange('currency_wage_id', 'wage_convert')
    def onchange_convert(self):
        if self.wage_convert and self.currency_wage_id:
            self.wage = self.currency_wage_id.rate * self.wage_convert

    @api.onchange('currency_wage_1_id', 'wage_1_convert')
    def onchange_convert_1(self):
        if self.wage_1_convert and self.currency_wage_1_id:
            self.wage_1 = self.currency_wage_1_id.rate * self.wage_1_convert
