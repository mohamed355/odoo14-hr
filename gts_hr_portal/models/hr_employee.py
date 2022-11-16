
from odoo import models, api, _
from odoo.tools import email_split
from odoo.exceptions import UserError


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ''


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)
        if not employee.user_id:
            user = employee.sudo()._create_user()
            group_portal = self.env.ref('base.group_portal')
            group_public = self.env.ref('base.group_public')
            user.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_public.id)]})
            employee.user_id = user.id
        return employee

    def _create_user(self):
        company = self.env.user.company_id
        company = self.company_id or company
        # print ("company========",company, self.company_id)
        return self.env['res.users'].with_context(no_reset_password=True).sudo()._create_user_from_template({
            'email': extract_email(self.work_email),
            'login': extract_email(self.work_email),
            'name': self.name,
            'partner_id': self.address_home_id and self.address_home_id.id or False,
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
        })
