{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Diego Vicuna",
    'category': "App",
    'application': True,
    'description': "This module doesnt do anything",
    'data' : [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/estate_property.xml',

        #Load initial Data
        'data/estate.property.csv'
    ]
}