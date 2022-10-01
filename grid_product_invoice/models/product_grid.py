from odoo import api, fields, models


class ProductGrid(models.TransientModel):
    _name = 'product.grid'
    _rec_name = 'name'

    name = fields.Char(default='Product Grid')
    product_id = fields.Many2one(comodel_name="product.template", string="Product Template", required=False, )
    pro_lines_ids = fields.One2many(comodel_name="product.grid.lines", inverse_name="product_grid_id", string="Lines",
                                    required=False, )

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.attribute_line_ids:
                for value in self.product_id.attribute_line_ids[0].value_ids:
                    self.env['product.grid.lines'].create({'product_grid_id': self.id, 'attribute_value_id': value.id})

    def create_invoice_line(self):
        invoice = self.env['account.move'].browse(self.env.context.get('active_ids'))
        for value in self.pro_lines_ids:
            print('%s (%s)' % (self.product_id.name, value.attribute_value_id.name))
            product = self.env['product.product'].search(
                [('product_template_variant_value_ids.name', '=', value.attribute_value_id.name)])
            print(product)
            fiscal_position = invoice.fiscal_position_id
            accounts = product.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
            if invoice.is_sale_document(include_receipts=True):
                # Out invoice.
                account = accounts['income'] or product.account_id
            elif invoice.is_purchase_document(include_receipts=True):
                # In invoice.
                account = accounts['expense'] or product.account_id
            account_move_obj = self.env['account.move.line'].with_context(check_move_validity=False).create(
                {'product_id': product.id, 'quantity': value.qty, 'move_id': invoice.id, 'account_id': account.id})
            account_move_obj._onchange_product_id()


class ProductGridLines(models.TransientModel):
    _name = 'product.grid.lines'

    product_grid_id = fields.Many2one(comodel_name="product.grid", string="Product Grid", required=False, )
    attribute_value_id = fields.Many2one(comodel_name="product.attribute.value", string="Value", required=False, )
    qty = fields.Float(string="Quantity", required=False, )
