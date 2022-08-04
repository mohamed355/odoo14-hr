from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AssignHiring(models.TransientModel):
    _name = 'assign.hiring'

    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", )

    def assign_hiring(self):
        applications = self.env['hr.applicant'].browse(self.env.context.get('active_ids'))
        for application in applications:
            for app in self.hiring_id.application_ids:
                if app.id == application.id:
                    raise ValidationError('This Application Already Assigned To %s ' % self.hiring_id.name)
            if application.hiring_ids:
                raise ValidationError('This Application Already In Hiring Request')
            self.hiring_id.update({'application_ids':[(4, application.id )]})
            application.update({'hiring_ids':[(4, self.hiring_id.id )]})