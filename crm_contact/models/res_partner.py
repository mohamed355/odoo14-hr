from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection(string="Type", selection=[('vendor', 'Vendor'), ('customer', 'Customer'),('contact', 'Contact') ], required=True, default='contact')
    lead_id = fields.Many2one(comodel_name="crm.lead", string="lead", required=False, )

    @api.onchange('contact_type')
    def _onchange_contact_type(self):
        if self.contact_type == 'vendor':
            self.customer_rank = 0
            self.supplier_rank = 1
        elif self.contact_type == 'customer':
            self.customer_rank = 1
            self.supplier_rank = 0

        elif self.contact_type == 'contact':
            self.customer_rank = 0
            self.supplier_rank = 0
