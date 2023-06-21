from odoo import api, fields, models, _


class Estate(models.Model):
    _name = "re.estate"
    _description = "here contains all informations about your estate"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    location_id = fields.Many2one('re.location', string='Location', required=False)
    tags = fields.Many2many('re.tag', string='tags ', required=False)

    state = fields.Selection(
        selection='_get_states',
        string='State',
        required=False,
        store=True
    )
    city = fields.Selection(
        selection='_get_cities',
        string='City',
        required=False
    )
    postal_code = fields.Selection(
        selection='_get_postal_codes',
        string='Postal Code',
        required=False
    )
    street = fields.Selection(
        selection='_get_streets',
        string='Street',
        required=False
    )

    @api.model
    def _get_states(self):
        locations = self.env['re.location'].sudo().search([])
        states = locations.mapped('state')
        distinct_states = list(set(states))
        return [(state, state) for state in distinct_states]

    @api.model
    def _get_cities(self):
        domain = [('state', '=', self.state)] if self.state else []
        locations = self.env['re.location'].sudo().search(domain)
        cities = locations.mapped('city')
        distinct_cities = list(set(cities))
        return [(city, city) for city in distinct_cities]

    @api.model
    def _get_postal_codes(self):
        domain = [('state', '=', self.state), ('city', '=', self.city)] if self.state and self.city else []
        locations = self.env['re.location'].sudo().search(domain)
        postal_codes = locations.mapped('postal_code')
        distinct_postal_codes = list(set(postal_codes))
        return [(postal_code, postal_code) for postal_code in distinct_postal_codes]

    @api.model
    def _get_streets(self):
        locations = self.env['re.location'].sudo().search([])
        streets = locations.mapped('street')
        distinct_streets = list(set(streets))
        return [(street, street) for street in distinct_streets]

    surface = fields.Char(string='Surface', required=False, tracking=True)
    price = fields.Integer(string='Price', tracking=True)

    @api.onchange('price_range')
    def _onchange_price_range(self):
        if self.price_range:
            self.price_min = self.price_range.lower
            self.price_max = self.price_range.upper
        else:
            self.price_min = False
            self.price_max = False

    type = fields.Selection([
        ('sale', 'Sale'),
        ('rent', 'Rent')
    ], string="Type", required=False, tracking=True)

    type_estate = fields.Selection([
        ('house', 'House'),
        ('land', 'Land'),
        ('apartement', 'Apartement')
    ], string="Type of estate", required=False, tracking=True)

    type_ground = fields.Char(string='Ground type', required=False, tracking=True)
    # the estate can have many images?
    image = fields.Image(string="uplod the Image from here ", max_width=100, max_height=100)

    # house properties
    agent = fields.Many2one('re.agent', string="Agent")
    owner = fields.Many2one('re.partner', string="Owner", domain="[('type', '=', 'owner')]")
    floor_nbr = fields.Char(string='number of floors', required=False, tracking=True)
    bedroom_nbr = fields.Char(string='number of bedrooms', required=False, tracking=True)
    bathroom_nbr = fields.Char(string='number of bathrooms', required=False, tracking=True)
    kitchen_nbr = fields.Char(string='number of kitchens', required=False, tracking=True)
    garden_surface = fields.Char(string='surface of the garden', tracking=True)

    # apartement number
    # house properties+ the fields below

    floor_num = fields.Char(string='current floor', required=False, tracking=True)

    ref = fields.Char(string='Order Reference', required=False,
                      readonly=True, default=lambda self: _('New'))

    # date of publication
    add_date = fields.Date(string='')

    # contract relation
    contract_id = fields.Many2one('re.contract', string='Contract')
    contract_line_ids = fields.One2many('re.contract', 'estate_id', string='Contract lines')

    @api.onchange('type')
    def _onchange_add_date(self):
        self.add_date = fields.Date.today()

    # disponibility date of the estate
    disponibility_date = fields.Date(string='Disponibility Date')

    def open_location_form(self):
        return {
            'res_model': 're.location',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('real_estate.view_re_location_form').id,
        }

    @api.model_create_multi
    def create(self, vals):
        for val in vals:

            location_values = {
                'state': val.get('state'),
                'city': val.get('city'),
                'postal_code': val.get('postal_code'),
                'street': val.get('street'),
            }

            location = self.env['re.location'].search([
                ('state', '=', location_values['state']),
                ('city', '=', location_values['city']),
                ('postal_code', '=', location_values['postal_code']),
                ('street', '=', location_values['street']),
            ], limit=1)
            if not location:
                location = self.env['re.location'].create(location_values)
            val['location_id'] = location.id
            val['ref'] = self.env['ir.sequence'].next_by_code('re.estate')
            return super(Estate, self).create(vals)

    def write(self, vals):
        location_values = {
            'state': vals.get('state', self.location_id.state),
            'city': vals.get('city', self.location_id.city),
            'postal_code': vals.get('postal_code', self.location_id.postal_code),
            'street': vals.get('street', self.location_id.street),
        }

        location = self.location_id
        if not location or any(location_values[field] != getattr(location, field) for field in location_values):
            location = self.env['re.location'].search([
                ('state', '=', location_values['state']),
                ('city', '=', location_values['city']),
                ('postal_code', '=', location_values['postal_code']),
                ('street', '=', location_values['street']),
            ], limit=1)
            if not location:
                location = self.env['re.location'].create(location_values)

        vals['location_id'] = location.id
        return super(Estate, self).write(vals)