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
        compute="_compute_video_source_type",
    )
    
    @api.depends('video_url', 'custom_video_source')
    def _compute_video_source_type(self):
        """Determine the video source type based on the video URL."""
        super()._compute_video_source_type()  # Call the original method to preserve existing logic
        for slide in self:
            if slide.video_source_type != 'custom' and slide.custom_video_source:
                slide.video_source_type = 'custom'

    @api.depends('slide_category', 'video_source_type', 'custom_video_source')
    def _compute_embed_code(self):
        """Compute the embed code based on custom video source."""
        super()._compute_embed_code()  # Call the original method to preserve existing logic
        for slide in self:
            embed_code = False
            embed_code_external = False
            if slide.video_source_type == 'custom':
                video_url = Markup('<iframe src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0" aria-label="%s"></iframe>')
                embed_code = video_url % (slide.video_url, 1600, 900, slide.video_title)
                
            slide.embed_code = embed_code
            slide.embed_code_external = embed_code
