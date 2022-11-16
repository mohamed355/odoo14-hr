{
    'name': 'Employee Join',
    'author': 'Ezzedin Saleh',
    'depends': ['base', 'hr', 'hr_contract', 'account', 'create_employee_applicant'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_join.xml',
        'views/employee_activity.xml',
        'views/hr_employee.xml',
    ],
}
