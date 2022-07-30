from odoo import api, fields, models, tools


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    # @api.model
    # def default_get(self, field_list):
    #     result = super(Applicant, self).default_get(field_list)
    #     if result['stage_id']:
    #         result['num'] = self.env['hr.recruitment.stage'].search([('id', '=', result['stage_id'])], limit=1).num_of_apps
    #     return result
    name = fields.Char("Subject / Application Name", required=False, help="Email subject for applications sent via email")

    hiring = fields.Integer(string="Hiring", required=False,store=True )
    # hiring_ids = fields.Many2many(comodel_name="hiring.request",  string="Hiring", )
    num = fields.Integer(string="Stage History", required=False ,store=True)

    # @api.depends()
    # def _compute_hiring(self):
    #     for x in self:
    #         app=self.env['hr.applicant'].search([('hiring','>',0)])
    #         if not app:
    #             x.hiring = self.env['hiring.request'].search_count([])
    #         if app:
    #             app.hiring = self.env['hiring.request'].search_count([])
    #         print(x.hiring)




class RecDashboard(models.Model):
    _name = 'rec.dashboard'
    _auto = False

    num = fields.Integer(string="Stage History", required=False , related='stage_id.num_of_apps')
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=False, )
    name = fields.Char(string="Name", required=False, )
    hiring_name = fields.Char(string="Hiring Name", required=False, )
    hi_create_date = fields.Char(string="Hiring Create Date", required=False, )
    create_date = fields.Datetime(string="App Create Date")
    apps = fields.Integer(string="Applications")
    hiring = fields.Integer(string="Hiring Requests",)
    stage_id = fields.Many2one(comodel_name="hr.recruitment.stage", string="Stage", required=False, )
    job_id = fields.Many2one(comodel_name="hr.job", string="Job")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Recruiter")
    source_id = fields.Many2one(comodel_name="utm.source", string="Source")
    # num1 =fields.Integer(string="Stage History", required=False)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        # Reference contract is the one with the latest start_date.
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, "SELECT count(hiring_request.*) as hiring,hiring_request.name as hiring_name,hiring_request.create_date as hi_create_date,hr_applicant.id as id,count(hr_applicant) as apps,hr_applicant.job_id as job_id,hr_applicant.partner_id as partner_id,hr_applicant.create_date as create_date,hr_applicant.name as name,hr_applicant.stage_id as stage_id,hr_applicant.source_id as source_id,hr_applicant.company_id as company_id FROM hr_applicant FULL OUTER JOIN hiring_request on hr_applicant.hiring = hiring_request.id GROUP BY hr_applicant.create_date,hr_applicant.name,hr_applicant.stage_id,hr_applicant.company_id,hr_applicant.id,hr_applicant.source_id,hiring_request.name,hiring_request.create_date"""))
        # #
        # self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, "SELECT count(*) as hiring FROM hiring_request """))





