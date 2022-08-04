from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    l_1_id = fields.Many2one(comodel_name="res.partner", string="Parent Company", )
    level_2_id = fields.Many2one(comodel_name="res.partner", string="Sector", )
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", )
    level_2_child = fields.One2many(comodel_name="res.partner", related="level_2_id.child_ids", required=True, )
    dep_child = fields.One2many(comodel_name="res.partner", related="partner_id.child_ids", required=True, )
    customer_child = fields.One2many(comodel_name="res.partner", related="l_1_id.child_ids", required=True, )
