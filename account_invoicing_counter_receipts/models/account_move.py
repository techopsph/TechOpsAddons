from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    counter_receipt_id = fields.Many2one(
        comodel_name='counter.receipts',
        string="Counter Receipt",
        required=False, ondelete='cascade', index=True, copy=False, readonly=True)
    
    counter_receipt_date = fields.Date(
        string='Counter Receipt Date', 
        related='counter_receipt_id.date')    
    
    