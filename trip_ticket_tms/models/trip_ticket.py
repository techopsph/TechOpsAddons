from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class TripTicket(models.Model):
    _name = "trip.ticket"
    _description = "Trip Ticket for Transport Management System to customers"
    _order = "create_date desc"
    _inherit = "mail.thread"
    
    name = fields.Char("Trip Ticket", default=lambda self: _('TRIP/'),
       copy=False, readonly=True, tracking=True)
    
    description = fields.Char(string="Description")

    company_id = fields.Many2one("res.company", 
                                string="Company")
    
    scheduled_date = fields.Date(string="Schedule Date", 
                                required=True, 
                                default=fields.Date.context_today)
    
    sequence = fields.Integer(string="Sequence", default=10)
    
    vehicle_id = fields.Many2one("fleet.vehicle",
                                 string="Vehicle")
    driver = fields.Many2one("res.partner",
                             string="Driver")
    helper = fields.Many2one("res.partner",
                             string="Helper")
    helper2 = fields.Many2one("res.partner",
                             string="Helper 2")
    helpers = fields.Many2many("res.partner",
                               string="Helpers")
    
    note = fields.Text(string="Note")
    
    
    loading_start_datetime = fields.Datetime(string="Loading Start")
    loading_end_datetime = fields.Datetime(string="Loading End")
    departure_datetime = fields.Datetime(string="Departure")
    arrival_datetime = fields.Datetime(string="Arrival")
    
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('confirm', "Confirmed"),
            ('loading_start', "Loading Start"),
            ('loading_end', "Loading End"),
            ('in_transit', "In Transit"),
            ('delivered', "Delivered"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
            ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    
    picking_ids = fields.One2many("stock.picking",
                                  "trip_ticket_id",
                                  string="Transfers")
    
    line_count = fields.Integer(compute="_compute_line_count")
    
    trip_sequence = fields.Selection(
        selection=[
            ('by_sequence', "By Sequence"),
            ('by_sales_order', "By Sales Order Number"),
            ],
        default="by_sequence",
        string="Trip Sequence",
    )
    
    @api.depends("picking_ids")
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.picking_ids)
            
            ## Recalculate the sequence of the trip tickets
            current_count = 1
            for trip in rec.picking_ids:
                trip = trip.ensure_one()
                if trip.trip_ticket_sequence == 1000:
                    trip.trip_ticket_sequence = current_count
                current_count = current_count + 1
    
    def action_draft(self):
        for rec in self:
            rec.state = "draft"
    
    def action_confirm(self):
        for rec in self:
            rec.state = "confirm"
    
    def action_loading_start(self):
        for rec in self:
            rec.state = "loading_start"
            rec.loading_start_datetime = fields.datetime.now()

    def action_loading_end(self):
        for rec in self:
            rec.state = "loading_end"
            rec.loading_end_datetime = fields.datetime.now()


    def action_in_transit(self):
        for rec in self:
            rec.state = "in_transit"
            rec.departure_datetime = fields.datetime.now()
    
    def action_delivered(self):
        for rec in self:
            rec.state = "delivered"
            rec.arrival_datetime = fields.datetime.now()
            
    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"
          
    def action_done(self):
        for rec in self:
            rec.state = 'done'
            for transfer in rec.picking_ids:
                transfer.button_validate()
            
    
    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('name', _('TRIP/')) == _('TRIP/'):
                vals['name'] = (self.env['ir.sequence'].
                next_by_code('trip.ticket'))
        return super().create(vals_list)