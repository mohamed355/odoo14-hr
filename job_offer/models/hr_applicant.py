from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    template = fields.Selection(string="Template", selection=[('ksa', 'KSA'), ('egy', 'EGY'), ('saudi', 'Saudi Offer Job')],
                                required=False, )
    offer_job_id = fields.Many2one(comodel_name="hr.job", string="Job Title", required=False, )
    package_salary = fields.Integer(string="Package", required=False, compute='_compute_package_salary')
    housing = fields.Integer(string="Housing", required=False, compute='_compute_package_salary')
    basic = fields.Integer(string="Basic", required=False, compute='_compute_package_salary')
    transportation = fields.Integer(string="Transportation", required=False, compute='_compute_package_salary')

    @api.depends('ex_of', 'ex_on', 'hiring_ids')
    def _compute_package_salary(self):
        for x in self:
            if x.hiring_ids:
                if x.hiring_ids[0].location == 'Egypt':
                    x.package_salary = x.ex_on
                    x.housing = 0
                    x.basic = 0
                    x.transportation = 0
                elif x.hiring_ids[0].location == 'Saudi Arabia':
                    x.package_salary = x.ex_of
                    x.basic = x.package_salary / 1.35
                    x.housing = x.basic / 4
                    x.transportation = x.basic / 10
                else:
                    x.package_salary = 0
                    x.housing = 0
                    x.basic = 0
                    x.transportation = 0
            else:
                x.package_salary = 0
                x.housing = 0
                x.basic = 0
                x.transportation = 0
