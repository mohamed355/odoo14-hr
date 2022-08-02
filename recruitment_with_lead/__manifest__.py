# -*- coding: utf-8 -*-
# Copyright (c) Open Value All Rights Reserved                     

{
    "name": "Recruitment with lead",
    "summary": '***********************************',
    "version": "12.0.1.0.0",
    "category": "Recruitment",
    "author": "Open Value",
    "support": 'mustafa.abdalrhman1@gmail.com',
    "license": "LGPL-3",
    "price": 00.00,
    "currency": 'EUR',
    "depends": [
        'crm', 'hr_recruitment',
    ],

    "data": [
        'security/ir.model.access.csv',
        "views/recruitment_w_lead_view.xml",
        # "data/ir_sequence.xml",

    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}

