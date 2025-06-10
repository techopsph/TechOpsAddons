from markupsafe import Markup
from odoo import models, fields, api

class Slide(models.Model):
    _inherit = 'slide.slide'

    video_source_type = fields.Selection(
        selection_add=[('custom', 'Custom')],
        ondelete={'custom': 'set default'},
    )

    embed_code_custom = fields.Html('Custom Embed Code', sanitize=False)
    
    @api.depends('slide_category', 'video_source_type', 'embed_code_custom', 'youtube_id')
    def _compute_embed_code(self):
        super()._compute_embed_code()  # preserve existing logic

        for slide in self:
            if slide.slide_category == 'video' and slide.video_source_type == 'custom' and slide.embed_code_custom:
                slide.embed_code = Markup(slide.embed_code_custom)
                slide.embed_code_external = slide.embed_code_custom