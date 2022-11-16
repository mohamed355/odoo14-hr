from odoo import api, fields, models


class EmployeeAct(models.Model):
    _name = 'emp.act'
    _rec_name = 'activity_type_id'
    activity_type_id = fields.Many2one(comodel_name="mail.activity.type", string="Activity Type", required=False, )
    description = fields.Text(string="Description", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="User", required=False, )
    hours = fields.Float(string="Hours", required=False, )
    template_id = fields.Many2one(comodel_name="template.act", string="Template", required=False, )
    internal = fields.Boolean(string="Internal", )


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    date_deadline = fields.Date('Due Date', index=True, required=True, default=fields.Date.context_today)


class Template(models.Model):
    _name = 'template.act'

    name = fields.Char()
