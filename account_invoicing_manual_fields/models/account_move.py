import datetime
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    sales_invoice_number = fields.Char(string='Sales Invoice Number', store=True)
    document_number = fields.Char(string='Document Number', store=True)
    remarks = fields.Text(string='Remarks', store=True)
    prepared_by = fields.Many2one('res.users', string='Prepared By', store=True)
    approved_by = fields.Many2one('res.users', string='Approved By', store=True)
    
    