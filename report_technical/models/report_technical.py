from odoo import api, fields, models, tools


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", required=False, )

    @api.onchange('hiring_ids')
    def onchange_hiring_ids(self):
        if self.hiring_ids:
            self.hiring_id = self.hiring_ids[0].id


class ReportTechnical(models.Model):
    _name = 'report.technical'
    _auto = False

    name = fields.Char(string="Name", required=False, )
    stage = fields.Char(string="Stage", required=False)
    hiring = fields.Char(string="Hiring", required=False)
    job_title = fields.Char(string="Job Title", required=False)
    location = fields.Char(string="Location", required=False)
    client = fields.Char(string="Client", required=False)
    serial = fields.Char(string="Serial", required=False)
    notice_period_from = fields.Integer(string="NP From", required=False)
    notice_period_to = fields.Integer(string="NP To", required=False)
    current_salary = fields.Integer(string="Current Salary", required=False)
    ex_salary = fields.Integer(string="Expected Salary", required=False)
    can_loc = fields.Char(string="Candidate Location", required=False)
    can_na = fields.Char(string="Candidate Nationality", required=False)
    interview_date = fields.Datetime(string="Interview Date", required=False)
    assign_to = fields.Char(string="Assigned Interviewer", required=False)
    interview = fields.Char(string="Interview", required=False)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                (
                    SELECT 
                    hr_applicant.id as id,
                    ' ' as interview,
                    hr_applicant.nationality as can_na,
                    hr_applicant.candidate_location as can_loc,
                    hr_applicant.app_code as serial,
                    hr_applicant.partner_name as name,
                    hr_applicant.interview_date as interview_date,
                    hr_applicant.inter_by as assign_to,
                    hr_applicant.notice_period_from as notice_period_from,
                    hr_applicant.notice_period_to as notice_period_to,
                    hr_applicant.current_salary as current_salary,
                    hr_applicant.ex_on + ex_of as ex_salary,
                    stage.name as stage,
                    hiring.name as hiring,
                    hiring.location as location,
                    hiring.client as client,
                    job.name as job_title
                    
                    FROM hr_applicant
                   	LEFT JOIN hiring_request hiring ON hiring.id = hr_applicant.hiring_id 
                   	LEFT JOIN hr_job job ON job.id = hiring.job_id 
                   	LEFT JOIN res_partner client ON client.id = hiring.client 
                    LEFT JOIN hr_recruitment_stage stage on stage.id = hr_applicant.stage_id

                    WHERE stage.name = 'Technical'
                                 )
            )
        """ % (self._table))
