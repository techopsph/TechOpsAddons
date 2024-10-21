from odoo import _, fields, models


class ResPartnerSocialMediaPlatform(models.Model):
    _name = "res.partner.socialmedia_platform"
    _description = "Social Media Platform"
    _order = "name"

    name = fields.Char(
        string="Platform Name",
        required=True,
        translate=True,
        help="Name of this Social Media Platform",
    )
    
    website = fields.Char(
        string="Website",
        required=True,
        help="Website URL of this Social Media Platform",
    )
    
    icon = fields.Char(
        string="Icon",
        help="Icon class name of this Social Media Platform",
    )