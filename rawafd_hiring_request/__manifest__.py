# -*- coding: utf-8 -*-
{
    'name': "rawafd_hiring_request",
    'depends': ['base', 'crm', 'hr_recruitment', 'recruitment_with_lead', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/ir_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}