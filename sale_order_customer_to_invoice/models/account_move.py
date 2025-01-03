from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_order_customer = fields.Many2one(
        "res.partner",
        string="Sale Order Customer",
        store=True,
        readonly=True,
        copy=True,
    )