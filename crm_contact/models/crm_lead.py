from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    contacts_ids = fields.One2many('res.partner', 'lead_id', string='Contacts', domain=[
        ('active', '=', True),('contact_type','=','contact')])
