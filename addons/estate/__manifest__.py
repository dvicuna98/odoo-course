{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base','mail'],
    'author': "Diego Vicuna",
    'category': "App",
    'application': True,
    'description': "This module doesnt do anything",
    'data' : [
        #Security
        'security/ir.model.access.csv',

        #Views
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_offer.xml',
        'views/menu.xml', # The order matter

        #Load initial Data
        'data/estate.property.csv',

        #scheduler
        'views/schedulers/estate_property_scheduler.xml',

        #Email templates
        'data/templates/example_email_template.xml'
    ]
}