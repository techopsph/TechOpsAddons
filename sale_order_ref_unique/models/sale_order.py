from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class SaleOrder(models.Model):
    _inherit = "sale.order"

    client_order_ref = fields.Char(copy=False)

    same_client_order_ref = fields.Many2one('sale.order', string='Sale Order with Customer Reference', compute='_compute_same_client_order_ref', store=False)

    @api.depends('partner_id', 'client_order_ref')
    def _compute_same_client_order_ref(self):
        for sale_order in self:
            sale_order_id = sale_order._origin.id
            ## Support for sale_isolated_quotation
            is_quotation = False
            if 'order_sequence' in sale_order:
                is_quotation = True
            SaleOrder = self.with_context(active_test=False).sudo()
            domain = [
                ('client_order_ref', '=', sale_order.client_order_ref),
            ]
            if sale_order.company_id:
                domain += [('company_id', 'in', [False, sale_order.company_id.id])]
            if sale_order_id and is_quotation:
                domain += [('id', '!=', sale_order_id), ('order_sequence', '!=', False)]
            if sale_order_id:
                domain += [('id', '!=', sale_order_id)] 
            sale_order.same_client_order_ref = bool(sale_order.client_order_ref) and SaleOrder.search(domain, limit=1)

    @api.constrains("client_order_ref")
    def _check_client_order_ref_unique(self):
        for record in self:
            if not record.client_order_ref:
                continue
            test_condition = config["test_enable"] and not self.env.context.get(
                "test_sale_order_ref"
            )
            if test_condition:
                continue
            if record.same_client_order_ref:
                raise ValidationError(
                    _("The Customer Reference %s already exists in another Sale Order.") % record.client_order_ref
                )
