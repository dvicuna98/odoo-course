from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'sequence, name'
    _sql_constraints = [
        ("check_name","UNIQUE(name)","The name must be unique")
    ]
    name = fields.Char('Name', required=True)
    sequence = fields.Integer("Sequence", default=10)

    property_ids = fields.One2many('estate.property','property_type_id', 'property_id')