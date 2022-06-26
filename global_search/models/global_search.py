from odoo import api, fields, models


class GlobalSearch(models.Model):
    _name = 'global.search'
    name = fields.Char(default="Search", required=False, )
    value = fields.Char(string="Search", required=True)
    crm_leads = fields.Many2many(comodel_name="crm.lead", relation="sdf", column1="df", column2="ffv", string="Leads",readonly=True, required=False, )
    partners = fields.Many2many(comodel_name="res.partner",  string="Partner",readonly=True, required=False, )
    crm_team = fields.Many2many(comodel_name="crm.team", relation="sdfs", column1="sdf", column2="sdfsf", string="Teams",readonly=True, required=False, )
    crm_tag = fields.Many2many(comodel_name="crm.tag", relation="dff", column1="sdfs", column2="fds", string="Tags",readonly=True, required=False, )
    crm_members = fields.Many2many(comodel_name="crm.team.member", relation="dddff", column1="sdf", column2="frg",readonly=True, string="Members", required=False, )
    crm_stage = fields.Many2many(comodel_name="crm.stage", relation="dvfv", column1="f", column2="df", readonly=True,string="Stage", required=False, )

    def search_records(self):
        for x in self:
            crm_leads = self.env['crm.lead'].search(['|','|',('name', 'ilike', x.value),('email_from', 'ilike', x.value),('contact_name', 'ilike', x.value)]).ids
            partners =self.env['res.partner'].search(['|','|',('name', 'ilike', x.value),('email','ilike',x.value),('mobile','ilike',x.value)]).ids
            crm_tag = self.env['crm.tag'].search([('name', 'ilike', x.value)]).ids
            crm_team = self.env['crm.team'].search([('name', 'ilike', x.value)]).ids
            crm_members = self.env['crm.team.member'].search(['|','|',('name', 'ilike', x.value),('email','ilike',x.value),('mobile','ilike',x.value)]).ids
            crm_stage = self.env['crm.stage'].search([('name', 'ilike', x.value)]).ids

            if  crm_leads:
                x.crm_leads = crm_leads
            if  partners:
                x.partners = partners
            if  crm_tag:
                x.crm_tag = crm_tag
            if crm_team:
                x.crm_team = crm_team
            if  crm_members:
                x.crm_members = crm_members
            if crm_stage:
                x.crm_stage = crm_stage



