from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_line_count = fields.Integer("Order Line Count", 
                                      compute="_compute_order_line_count", 
                                      store=True,
                                      readonly=True,
                                      help="Number of order lines in the sale order")
    
    @api.depends("order_line")
    def _compute_order_line_count(self):
        for record in self:
            record.order_line_count = len(record.order_line.filtered(lambda x: x.display_type == False))