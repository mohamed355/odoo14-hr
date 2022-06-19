# -*- coding: utf-8 -*-
{
    "name": "Partner Organization Chart",
    "summary": """Organization Chart Widget for Partner""",
    "description": """Organization Chart Widget for Partner""",
    "depends": ["base", "contacts",'web'],
    "author": "Moltis Technologies, Odoo SA",
    "website": "www.moltis.net",
    "support": "info@moltis.net",
    "category": "Tools",
    "version": "13.0.0.1",
    "data": [
        # "views/partner_templates.xml",
        "views/partner_views.xml"
    ],
    "qweb": [
        "static/src/xml/partner_org_chart.xml",
    ],
    "images": ["static/description/banner.png"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,

'web.assets_backend': [
            ('include', 'web._assets_helpers'),
            ('include', 'web._assets_backend_helpers'),

            '/partner_org_chart/static/src/scss/variables.scss',
'/partner_org_chart/static/src/scss/partner_org_chart.scss',
    '/partner_org_chart/static/src/js/partner_org_chart.js']
}
