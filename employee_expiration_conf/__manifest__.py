{
    'name': 'Employee Expiration Configuration',
    'author': 'Ezzedin Saleh',
    'depends': ['base', 'hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/expiration_conf.xml',
        'data/cron_job.xml',
    ],
}
