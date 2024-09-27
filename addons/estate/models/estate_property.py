from email.policy import default

from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstateProperty'

    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'The name must be unique'
        ),
        (
            'check_percentage',
            'CHECK(facades >= 0 and facades <= 100)',
            'The number input should be between 0 and 100'
        )
    ]

    # @api.constrains('date_end')
    # def _check_date_end(self):
    #     for record in self:
    #         if record.date_end < fields.Date.today():
    #             raise ValidationError("The end date cannot be set in the past.")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError('The selling_price must be positive')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # @api.depends('offer_ids.price')
    # def _compute_price(self):
    #     for prop in self:
    #         prop.best_price = max(prop.offer_ids.price, prop.price)

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties are not be sold")
        return self.write({'state': 'sold'})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
                raise UserError("Sold properties are not to be canceled")

        return self.write({'state': 'canceled'})

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', default="Estate description")
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("N", "North"),("S", "South"),("E", "East"),("W", "West")],
    )
    last_seen = fields.Datetime(string='Last Seen', default=fields.Datetime.now())

    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True, copy=False)

    total_area = fields.Integer(string='Total Area', readonly=True, compute="_compute_total_area")
    state = fields.Selection(
        selection=[
            ("new","New"),
            ("offer_received","Offer Received"),
            ("offer_accepted","Offer Accepted"),
            ("sold","Sold"),
            ("canceled","Canceled"),
        ],
        string='Status',
        required=True,
        default='new',
        copy=False,
    )