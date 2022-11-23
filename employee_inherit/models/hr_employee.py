from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_leave_in_id = fields.Many2one(comodel_name="hr.leave.in", string="Live", required=False, )
    visa_type_id = fields.Many2one(comodel_name="visa.type", string="Visa Type", required=False, )
    boundaries_id = fields.Many2one(comodel_name="boundaries", string="Boundaries N", required=False, )
    accommodation_id = fields.Many2one(comodel_name="accommodation", string="Accommodation N", required=False, )
    acc_date = fields.Date(string="Accommodation date", required=False, )
    social_insurance = fields.Char(string="Social insurance", required=False, )
    medical_in = fields.Char(string="Medical insurance", required=False, )
    taxes = fields.Char(string="Taxes", required=False, )


class VisaType(models.Model):
    _name = 'visa.type'

    name = fields.Char()


class Boundaries(models.Model):
    _name = 'boundaries'

    name = fields.Char()


class Accommodation(models.Model):
    _name = 'accommodation'

    name = fields.Char()
