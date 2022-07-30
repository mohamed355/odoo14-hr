{
    'name': 'Recruitment Dashboard',
    'author': 'EzzEdin Saleh',
    'depends': ['base','hr_recruitment','rawafd_hiring_request'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard.xml',
             ],


    # 'assets': {
    #     'web.assets_backend': [
    #
    #         'crm_dashboard_module/static/css/style.css',
    #         'crm_dashboard_module/static/css/style.scss',
    #         'recruitment_dashboard/static/js/dashboard.js',
    #         'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
    #
    #
    #         ],
    #     'web.assets_qweb': [
    #         'recruitment_dashboard/static/xml/dashboard.xml',
    #     ],
    # },
}