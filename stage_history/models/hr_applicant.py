from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    stages_ids = fields.Many2many(comodel_name="hr.recruitment.stage", relation="relationstage", column1="relation", column2="stage", string="Stage History", )
    admin_boolean = fields.Boolean("Admin" , compute='_compute_admin')
    @api.constrains('stage_id')
    def _onchange_stage_id(self):
        self.update({'stages_ids': [(4, self.stage_id.id)]})

    # @api.onchange('stage_id')
    # def _onchange_stage_id(self):
    #     self.update({'stages_ids': [(4, self.stage_id.id)]})
    @api.depends()
    def _compute_admin(self):
        for x in self:
            if self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
                x.admin_boolean = True
            else:
                x.admin_boolean = False

class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'
    num_of_apps = fields.Integer(string="Applications N", required=False, compute='_compute_num_of_apps')

    @api.depends()
    def _compute_num_of_apps(self):
        for x in self:
            applications = self.env['hr.applicant'].search([])
            num_of_apps=0
            for app in applications:
                if x.id in app.stages_ids.ids:
                    num_of_apps+=1

            x.num_of_apps = num_of_apps