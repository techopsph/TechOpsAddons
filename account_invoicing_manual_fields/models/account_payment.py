import datetime
from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    provisional_receipt_number = fields.Char(string='Provisional Receipt Number', store=True)
    collection_receipt_number = fields.Char(string='Collection Receipt Number', store=True)
    
    