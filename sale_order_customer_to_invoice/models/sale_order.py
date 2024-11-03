from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals["sale_order_customer"] = self.partner_id.id
        return vals