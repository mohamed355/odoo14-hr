{
    'name': 'Employee Join',
    'author': 'Ezzedin Saleh',
    'depends': ['base', 'hr', 'hr_contract', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_join.xml',
        'views/hr_employee.xml',
    ],
}
