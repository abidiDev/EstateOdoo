from odoo import api, fields, models, _

class EstateTag(models.Model):
    _name = "re.tag"
    _description = "here contains some tags that you can put in estates"
    _inherit = ['mail.thread','mail.activity.mixin']