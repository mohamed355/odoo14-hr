from odoo import api, fields, models, tools


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    is_tec = fields.Boolean(string="Technical", )

    @api.constrains('stage_id')
    def constrains_stage_id(self):
        if self.stage_id.name == 'Technical Interview':
            self.is_tec = True
            if self.hiring_ids:
                self.env['report.technical.app'].create({
                    'name': self.partner_name,
                    'stage': self.stage_id.name,
                    'hiring': self.hiring_ids[0].name,
                    'job_title': self.hiring_ids[0].job_id.name,
                    'location': self.hiring_ids[0].location,
                    # 'client': self.hiring_ids[0].client.name,
                    'serial': self.app_code,
                    'notice_period_from': self.notice_period_from,
                    'notice_period_to': self.notice_period_to,
                    'current_salary': self.current_salary,
                    'ex_salary': self.ex_of + self.ex_on,
                    'can_loc': self.candidate_location,
                    'can_na': self.nationality,
                    'interview_date': self.interview_date,
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
                    # 'client': self.hiring_ids[0].client.name,
                    'serial': self.app_code,
                    'notice_period_from': self.notice_period_from,
                    'notice_period_to': self.notice_period_to,
                    'current_salary': self.current_salary,
                    'ex_salary': self.ex_of + self.ex_on,
                    'can_loc': self.candidate_location,
                    'can_na': self.nationality,
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
    meeting_id = fields.Many2one(comodel_name="calendar.event", string="Meeting", required=False,
                                 compute='_compute_meeting')
    interview = fields.Selection(string="Interview",
                                 selection=[('invited', 'Invited'), ('attend', 'Attend'), ('no', 'No Show'),
                                            ('passed', 'Passed'), ('failed', 'Failed'), ('waiting', 'Waiting'),
                                            ('app', 'Apologized'), ('re', 'Reschedule'), ('pos', 'Postponed')],
                                 required=False, )

    changed = fields.Boolean(string="Changed", )

    @api.onchange('interview_date')
    def onchange_interview_date(self):
        if self.interview_date:
            self.changed = True

    def create_meeting(self):
        self.changed = False
        return {
            'name': 'Meeting',
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'context': {
                'default_start': self.interview_date,
                'default_start_date': self.interview_date,
                'default_end': self.interview_date,
                'default_end_date': self.interview_date,
                'default_interview_id': self.id
            },
            'target': 'new',
        }

    @api.depends()
    def _compute_meeting(self):
        for x in self:
            meeting = self.env['calendar.event'].search([('interview_id', '=', x.id)], order='create_date asc')
            print(meeting.mapped('name'))
            if meeting:
                x.meeting_id = meeting[-1].id

    def open_meeting(self):
        return {
            'name': 'Meeting',
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.meeting_id.id)]
        }


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    interview_id = fields.Many2one(comodel_name="report.technical.app", string="Interview", required=False, )
