{
    'name': 'Real Estate Management System',
    'version': '1.0',
    'summary': 'Real Estate Management System',
    'sequence': 1,
    'depends': ['base', 'mail'],
    'data': [
        "security/ir.model.access.csv",
        'views/menu.xml',
        'views/adds.xml',
        'views/location.xml',
        'data/sequence.xml'

    ],
    'installable': True,
    'auto_install': True,
}