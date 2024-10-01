from email.policy import default

from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price',"CHECK(price > 0)","Price must be greater than 0"),
    ]

    price = fields.Float("price", required=True)
    validity = fields.Integer("Validity (Days)", default=7)

    state = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        default=False,
        copy=False
    )

    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property", string="Property",required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
