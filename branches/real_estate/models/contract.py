from datetime import date, datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ReContract(models.Model):
    _name = 're.contract'

    owner = fields.Many2one('re.estate', string="Owner")
    lodger = fields.Many2one('re.partner', string="Lodger", domain="[('type', '=', 'lodger')]", required=True,
                             tracking=True)
    f_price = fields.Float(string="Final Price", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True, tracking=True)
    end_date = fields.Date(string="End date", required=True, tracking=True)
    creation_date = fields.Date(string="Creation Date")

    estate_id = fields.Many2one('re.estate', string='Estate')

    ref = fields.Char(string='Reference', readonly=True, default=lambda self: _('New'))

    # Remplissage auto du champs creation_date
    @api.onchange('ref')
    def _onchange_date(self):
        if self.ref != "":
            self.creation_date = date.today().strftime('%Y-%m-%d')
    #
    # @api.onchange('end_date')
    # def _onchange_empty(self):
    #     current_date = datetime.now().date()
    #     if self.end_date < current_date:
    #         self.empty = True
    #     else:
    #         self.empty = False

    # Contrôle de saisie contract
    @api.constrains('end_date', 'start_date', 'creation_date', 'f_price')
    def date_constrains(self):
        for rec in self:
            if rec.creation_date > rec.start_date:
                raise ValidationError(_('Sorry, Start Date Must be equal or greater Than Creation Date'))
            elif rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date'))
            elif rec.f_price < 0.0:
                raise ValidationError(_('Sorry, Price field is incorrect'))

    # Sequence contrat
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['ref'] = self.env['ir.sequence'].next_by_code('re.contract')
            val['owner'] = self.owner
        return super(ReContract, self).create(vals)
