from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'EstateProperty'
    _order = "date_availability desc"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name must be unique'),
        ('check_percentage', 'CHECK(facades >= 0 and facades <= 100)', 'Facades must be between 0 and 100'),
    ]

    @api.model
    def create(self, vals):
        if vals.get("selling_price") and vals.get("date_availability"):
            vals["state"] = "offer_received"
        return super(EstateProperty, self).create(vals)

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties are not be sold")
        return self.write({'state': 'sold'})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
                raise UserError("Sold properties are not to be canceled")

        return self.write({'state': 'canceled'})

    def action_send_email(self):
        template = self.env.ref["estate.simple_example_email_template"]
        email_values = {
            "email_to": "howace3333@aiworldx.com",
            "email_cc": False,
            "auto_delete": True,
            "recipient_ids": [],
            "partner_ids": [],
            "scheduled_date": False,
            "email_from":"howace3333@aiworldx.com"
        }
        template.send_mail(
            self.id,
            email_values = email_values,
            force_send = True
        )

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', default="Estate description")
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected Price', default=0.0)
    selling_price = fields.Float(string='Selling Price', default=0.0)
    bedrooms = fields.Integer(string='Bedrooms', default=0)
    living_area = fields.Integer(string='Living Area', default=0)
    facades = fields.Integer(string='Facades', default=0)
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area', default=0)
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
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string='Status',
        required=True,
        default='new',
        copy=False,
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offer')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = (prop.living_area or 0) + (prop.garden_area or 0)

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError('The selling_price must be positive')

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def update_state_schedule(self):
        self.env["estate.property"].search([('date_availability', '=', False)]).write({'state': 'new'})


    # @api.depends('offer_ids.price')
    # def _compute_price(self):
    #     for prop in self:
    #         prop.best_price = max(prop.offer_ids.price, prop.price)

