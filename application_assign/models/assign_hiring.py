from odoo import api, fields, models
from odoo.exceptions import ValidationError



class AssignHiring(models.TransientModel):
    _name = 'assign.hiring'

    hiring_ids = fields.Many2many(comodel_name="hiring.request", relation="hiringrequest", column1="hiring", column2="request", string="Hiring", )

    def assign_hiring(self):
        applications = self.env['hr.applicant'].browse(self.env.context.get('active_ids'))
        for hiring in self.hiring_ids:
            for application in applications:
                for app in hiring.application_ids:
                    if app.id == application.id:
                        raise ValidationError('This Application Already Assigned To %s ' % hiring.name)
                        break
                hiring.update({'application_ids':[(4, application.id )]})