from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    trip_ticket_id = fields.Many2one(
        comodel_name='trip.ticket',
        string="Trip Ticket",
        required=False, index=True, copy=False)
    
    trip_ticket_sequence = fields.Integer(compute='_compute_sequence',
                              store=True, 
                              readonly=False, 
                              precompute=True,
                              default=1000,
                              tracking=3)
    
    trip_ticket_scheduled_date = fields.Date(
        related='trip_ticket_id.scheduled_date')
    
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
    
    sale_order_customer = fields.Many2one("res.partner",
                                            string="Sale Order Customer",
                                            store=True,
                                            readonly=True,
                                            copy=True)
     
    
    def _compute_sequence(self):
        for rec in self:
            if rec.trip_ticket_sequence < 1:
                rec.trip_ticket_sequence = 1000
            if rec.trip_ticket_id:
                rec.trip_ticket_sequence = 1000
                
    
    @api.depends('sale_id')
    def _compute_sale_order_customer(self):
        for rec in self:
            rec.sale_order_customer = rec.sale_id.partner_id
    
    @api.depends('trip_ticket_id')
    def _compute_trip_ticket_fields(self):
        for rec in self:
            rec.vehicle_id = rec.trip_ticket_id.vehicle_id
            rec.driver = rec.trip_ticket_id.driver
            rec.helper = rec.trip_ticket_id.helper
            rec.helper2 = rec.trip_ticket_id.helper2
            rec.helpers = rec.trip_ticket_id.helpers