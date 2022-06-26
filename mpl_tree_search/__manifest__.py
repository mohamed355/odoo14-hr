# -*- coding: utf-8 -*-
###############################################################################
#
#    Meghsundar Private Limited(<https://www.meghsundar.com>).
#
###############################################################################
{
    'name': 'General Search in Tree View',
    'version': '14.0.1',
    'summary': 'General Search in Tree View',
    'description': 'User allow to search for all fields value in tree view.',
    'license': 'AGPL-3',
    'author': 'Meghsundar Private Limited',
    'website': 'https://meghsundar.com',
    'depends': ['base'],
    'category': 'Extra Tools',
    'data': [
        # 'views/view_assets.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {

        'web.assets_backend': [
            '/mpl_tree_search/static/src/js/search_list.js',
            'mpl_tree_search/static/src/css/search_list.css',
        ],
    },
    'images': ['static/description/banner.gif'],
}
