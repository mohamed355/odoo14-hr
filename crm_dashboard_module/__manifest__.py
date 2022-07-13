{
    'name': 'Crm Dashboard',
    'author': 'EzzEdin Saleh',
    'depends': ['crm'],
    'data': ['views/dashboard.xml'],


    'assets': {
        'web.assets_backend': [

            'crm_dashboard_module/static/css/style.css',
            'crm_dashboard_module/static/css/style.scss',
            'crm_dashboard_module/static/js/dashboard.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            'crm_dashboard_module/static/js/lib/highcharts.js',
            'crm_dashboard_module/static/js/lib/Chart.bundle.js',
            'crm_dashboard_module/static/js/lib/funnel.js',
            'crm_dashboard_module/static/js/lib/d3.min.js',
            'crm_dashboard_module/static/js/lib/material-gauge.js',
            'crm_dashboard_module/static/js/lib/columnHeatmap.min.js',
            'crm_dashboard_module/static/js/lib/columnHeatmap.js',

            ],
        'web.assets_qweb': [
            'crm_dashboard_module/static/xml/dashboard.xml',
            # 'crm_dashboard/static/src/xml/sub_dashboard.xml',
        ],
    },
}