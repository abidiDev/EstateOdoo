from odoo import models, fields, api, _


class RePartner(models.Model):
    _name = 're.partner'
    _inherit = ['mail.thread']
    _ref_name = 'name'

    name = fields.Char(string="Name", required=True)
    tel = fields.Char(string="Tel", required=True)
    email = fields.Char(string="Email", required=True)
    address = fields.Char(string="Address", required=True)
    image = fields.Image(string="Image")
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    type = fields.Selection([
        ('lodger', 'Lodger'),
        ('owner', 'Owner')
    ], string="Type", required=True, tracking=True)
    title = fields.Many2one('res.partner.title', string="Title", tracking=True)
    note = fields.Text(string='description', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner')

    # Creation sequence & res.partner
    @api.model_create_multi
    def create(self, vals_list):
        partners = self.env['res.partner']
        n_partners = self.env['re.partner']

        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('re.partner')
            partner = partners.create({'name': vals.get('name')})
            vals['partner_id'] = partner.id
            n_partners += super(RePartner, self).create(vals)

        return n_partners