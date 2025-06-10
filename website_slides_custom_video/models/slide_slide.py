from markupsafe import Markup
from odoo import models, fields, api

class Slide(models.Model):
    _inherit = 'slide.slide'

    custom_video_source = fields.Boolean(
        string='Custom Video Source',
        help='Enable custom video source for this slide.',
        default=False,
    )

    video_source_type = fields.Selection(
        selection_add=[('custom', 'Custom')],
        ondelete={'custom': 'set null'},
    )

    embed_code_custom = fields.Html('Custom Embed Code', sanitize=False)
    
    @api.depends('slide_category', 'video_source_type', 'embed_code_custom', 'custom_video_source')
    def _compute_embed_code(self):
        """Compute the embed code based on custom video source."""
        super()._compute_embed_code()  # Call the original method to preserve existing logic
        for slide in self:
            if slide.slide_category == 'video' and slide.embed_code_custom:
                slide.video_source_type == 'custom'
                slide.embed_code = Markup(slide.embed_code_custom)
                slide.embed_code_external = slide.embed_code_custom
