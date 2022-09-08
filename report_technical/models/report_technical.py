from odoo import api, fields, models, tools


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    is_tec = fields.Boolean(string="Technical",  )

    @api.constrains('stage_id')
    def constrains_stage_id(self):
        if self.stage_id.name == 'Technical Interview':
            self.is_tec = True
            if self.hiring_ids:
                self.env['report.technical.app'].create({
                    'name':self.partner_name,
                    'stage':self.stage_id.name,
                    'hiring':self.hiring_ids[0].name,
                    'job_title':self.hiring_ids[0].job_id.name,
                    'location':self.hiring_ids[0].location,
                    'client':self.hiring_ids[0].client.name,
                    'serial':self.app_code,
                    'notice_period_from':self.notice_period_from,
                    'notice_period_to':self.notice_period_to,
                    'current_salary':self.current_salary,
                    'ex_salary':self.ex_of + self.ex_on,
                    'can_loc':self.candidate_location,
                    'can_na':self.nationality,
                    'interview_date':self.interview_date,
                })


    @api.constrains('hiring_ids')
    def constrains_hiring(self):
        if self.hiring_ids:
            if self.is_tec == True:
                self.env['report.technical.app'].create({
                    'name': self.partner_name,
                    'stage': self.stage_id.name,
                    'hiring': self.hiring_ids[0].name,
                    'job_title': self.hiring_ids[0].job_id.name,
                    'location': self.hiring_ids[0].location,
                    'client': self.hiring_ids[0].client.name,
                    'serial': self.app_code,
                    'notice_period_from': self.notice_period_from,
                    'notice_period_to': self.notice_period_to,
                    'current_salary': self.current_salary,
                    'ex_salary': self.ex_of + self.ex_on,
                    'can_loc': self.candidate_location,
                    'can_na': self.nationality,
                    'interview_date': self.interview_date,
                })


class ReportTechnicalApp(models.Model):
    _name = 'report.technical.app'

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
    notes = fields.Char(string="Notes", required=False)
    # interview = fields.Char(string="Interview", required=False)
    interview = fields.Selection(string="Interview", selection=[('invited', 'Invited'), ('attend', 'Attend'), ('no', 'No Show'), ('passed', 'Passed'), ('failed', 'Failed'), ('waiting', 'Waiting'), ('app', 'Apologized'), ('re', 'Reschedule'), ('pos', 'Postponed') ], required=False, )