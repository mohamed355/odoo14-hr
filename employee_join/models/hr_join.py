from odoo import api, fields, models


class HrJoin(models.Model):
    _name = 'hr.join'

    name = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False,
                                    related='name.department_id',
                                    store=True)
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    job_position = fields.Many2one('hr.job', related="name.job_id", readonly=True, string="Job Position",
                                   help="Job position")
    manager_id = fields.Many2one('hr.employee', string="Manager", related='name.parent_id', readonly=False,
                                 store=True, )
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', )
    company_id = fields.Many2one('res.company', string='Analytic Account', related='name.company_id', store=True)
    sales_price = fields.Float(string="Sales Price", required=False, )
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('approved', 'Approved'), ],
                             required=False, default='draft')

    @api.model
    def create(self, values):
        res = super(HrJoin, self).create(values)
        for record in res:
            if record.product_id:
                if record.analytic_account_id:
                    self.env['account.analytic.default'].create(
                        {'analytic_id': record.analytic_account_id.id, 'product_id': record.product_id.id})

        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.sales_price = self.product_id.list_price

    def approved(self):
        self.state = 'approved'

    def create_contract(self):
        return {
            'name': 'Create Contract',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.contract',
            'type': 'ir.actions.act_window',
            'context': {
                'default_employee_id': self.name.id,
            },
            'target': 'new'

        }
