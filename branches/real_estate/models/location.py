from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Location(models.Model):
        _name = "re.location"
        _description = "here contains all informations about your estate locations"
        _inherit = ['mail.thread', 'mail.activity.mixin']
        state = fields.Char(string='State', required=False, tracking=True)
        city = fields.Char(string='city', tracking=True)
        postal_code = fields.Char(string='postal code', tracking=True)
        street = fields.Char(string='Street Name', tracking=True)
        ref = fields.Char(string='Order Reference', required=False,
                          readonly=True, default=lambda self: _('New'))
        def name_get(self):
                res = []
                for rec in self:
                 res.append((rec.id, "%s, %s" % (rec.state, rec.city)))
                return res

        @api.model_create_multi
        def create(self, vals):
                for val in vals:
                        val['ref'] = self.env['ir.sequence'].next_by_code('re.location')
                return super(Location, self).create(vals)