from odoo import _, fields, models, api
from odoo.exceptions import UserError

class CounterReceipts(models.Model):
    "Counter Receipts for grouping Customer Invoices or Vendor Bills"
    _name = "counter.receipts"
    _description = "Counter Receipts"
    _order = "date desc"
    _inherit = "mail.thread"
    
    name = fields.Char("Counter Receipt", default=lambda self: _('COUNTER/'),
       copy=False, readonly=True, tracking=True)
    
    date = fields.Date(string='Date')
    collector = fields.Many2one('res.partner', string='Collector')
    counter_receipt_number = fields.Char(string='Counter Receipt Number')
    
    line_count = fields.Integer(string='Line Count', compute='_compute_line_count')
    
    move_ids = fields.Many2many('account.move', 
                                string='Account Moves')
    
    note = fields.Text(string='Notes')
    partner_id = fields.Many2one('res.partner', string='Customer')
    prepared_by = fields.Many2one('res.users', string='Prepared By')
    received_by = fields.Many2one('res.partner', string='Received By')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    
        
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.move_ids)
            
    def action_confirm(self):
        for record in self:
            record.state = 'in_progress'
            self.set_counter_receipt()
    
    def action_done(self):
        for record in self:
            record.state = 'done' 
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
            # Unset counter_receipt_id on all linked account.move entries
            record.move_ids.write({'counter_receipt_id': False})
            
    def action_draft(self):
        for record in self:
            record.state = 'draft'
            # Unset counter_receipt_id on all linked account.move entries
            record.move_ids.write({'counter_receipt_id': False})


    def print_counter_receipts(self):
        report_action = self.env.ref('account_invoicing_counter_receipts.action_report_counter_receipts')
        return report_action.report_action(self)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('COUNTER/')) == _('COUNTER/'):
                vals['name'] = (self.env['ir.sequence'].
                next_by_code('counter.receipts'))
        return super().create(vals_list)

    def write(self, vals):
        if 'move_ids' in vals:
            for record in self:
                # Get original move_ids
                old_moves = record.move_ids

                # Simulate the new move_ids after update
                new_moves = self.browse([])  # default empty
                move_commands = vals.get('move_ids', [])
                if move_commands:
                    new_moves = old_moves.browse([cmd[1] for cmd in move_commands if cmd[0] == 4])
                    if any(cmd[0] == 6 for cmd in move_commands):
                        move_ids = [cmd[2] for cmd in move_commands if cmd[0] == 6][0]
                        new_moves = self.env['account.move'].browse(move_ids)

                # Find moves that were removed
                removed_moves = old_moves - new_moves

                # Unset their counter_receipt_id
                removed_moves.write({'counter_receipt_id': False})

        return super(CounterReceipts, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state not in ('draft', 'cancel'):
                raise UserError(_('You cannot delete a Counter Receipt that is not in draft or cancelled state.'))
        return super(CounterReceipts, self).unlink()
    
    def set_counter_receipt(self):
        for record in self:
            for move in record.move_ids:
                move.counter_receipt_id = record.id
        return True