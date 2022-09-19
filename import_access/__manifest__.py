{
    'name': 'Import Applicant Access',
    'author': 'Ezzedin Saleh',
    'depends': ['base_import', 'hr_recruitment'],
    'data': ['security/security.xml'],
    'assets': {
        'web.assets_backend': [
            'import_access/static/js/import.js',
        ],
    },
}
