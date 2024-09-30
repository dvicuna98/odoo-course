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
        'views/menu.xml',
        'views/estate_property.xml',

        #Load initial Data
        'data/estate.property.csv',

        #scheduler
        'views/schedulers/estate_property_scheduler.xml',

        #Email templates
        'data/templates/example_email_template.xml'
    ]
}