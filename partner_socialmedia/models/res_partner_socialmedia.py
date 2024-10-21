from odoo import api, fields, models


class ResPartnerSocialMedia(models.Model):
    _name = "res.partner.socialmedia"
    _description = "Partner Social Media"
    _order = "name"

    name = fields.Char(
        string="Social Media Account",
        required=True,
        help="The Social Media Account username or contact",
    )
    
    account_id = fields.Char(
        string="Account ID",
        help="The Social Media Account ID",
    )
    
    platform_id = fields.Many2one(
        string="Platform",
        required=True,
        comodel_name="res.partner.socialmedia_platform",
        help="Social Medial platform defined in configuration. For example, Facebook, Twitter etc",
    )
    
    full_url = fields.Char(
        string="Full URL",
        compute="_compute_full_url",
        help="Full URL of the Social Media Account",
    )
    
    full_url_manual = fields.Char(
        string="Full URL Manual",
        help="Full URL of the Social Media Account",
    )
    
    partner_id = fields.Many2one(
        string="Partner", required=True, comodel_name="res.partner", ondelete="cascade"
    )
    
    active = fields.Boolean(default=True)
    
    @api.depends("name", "platform_id", "platform_id.website", "full_url_manual")
    def _compute_full_url(self):
        for rec in self:
            if rec.full_url_manual:
                rec.full_url = rec.full_url_manual
            else:
                if rec.platform_id.website and rec.name:
                    rec.full_url = rec.platform_id.website + "/" + rec.name
                else:
                    rec.full_url = False
            