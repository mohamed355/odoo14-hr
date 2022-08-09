# Part of Warlock. See LICENSE file for full copyright and licensing details.
{
    'name': 'GS Portal Attemdances',
    'version': '15.0.1',
    'category': 'Human Resources/Attendances',
    "author": "Global Solutions",
    "website": "https://globalsolutions.dev",
    'sequence': 365,
    'summary': 'WT Portal Attemdances',
    'description': """WT Portal Attemdances""",
    'depends': ['hr_attendance', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/portal_attendance.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'gs_portal_attendances/static/src/scss/attendance.scss',
            'gs_portal_attendances/static/src/js/attendance.js'
        ],
        'web.assets_qweb': [
            'gs_portal_attendances/static/src/xml/attendance.xml',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
