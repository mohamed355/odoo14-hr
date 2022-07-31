{
    'name': 'Recruitment Dashboard',
    'author': 'EzzEdin Saleh',
    'depends': ['hr_recruitment'],
    'data': ['views/dashboard.xml'],


    'assets': {
        'web.assets_backend': [

            'crm_dashboard_module/static/css/style.css',
            'crm_dashboard_module/static/css/style.scss',
            'recruitment_dashboard/static/js/dashboard.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',


            ],
        'web.assets_qweb': [
            'recruitment_dashboard/static/xml/dashboard.xml',
        ],
    },
}