# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo import models, fields, api, _
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from lxml import etree


class HrApp(models.Model):
    _inherit = 'hr.applicant'

    _sql_constraints = [('email_from_uniq', 'CHECK (1=1)', 'Email is Duplicated')]

    re_action = fields.Char(string="Recommended Action", required=False, )
    last_update_applicant = fields.Date(string="Last Update", required=False, )
    app_code = fields.Char(string="Serial", required=False)
    # notes = fields.Text(string="Notes", required=False, )
    ref_employee_id = fields.Many2one(comodel_name="hr.employee", string="Referred By Employee", required=False, )
    acc_date = fields.Date(string="Accepted Date", required=False, )
    ex_of = fields.Float(string="Expected(Offshore)", required=False, )
    ex_on = fields.Float(string="Expected(Onsite)", required=False, )
    current_salary = fields.Float(string="Current Salary", required=False, )
    stage_date = fields.Datetime(string="Stage Time", required=False, )
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    language_ids = fields.Many2many('job.lang')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender')
    experience_level = fields.Selection([
        ('intern', 'Intern'), ('fresh', 'Fresh'), ('jr', 'Junior'), ('senior', 'Senior'), ('teamlead', 'Team Lead'),
        ('manager', 'Manager'), ('consultant', 'Consultant')
    ], string='Experience level')
    linkedin = fields.Char(string="Linkedin", required=False, )
    first_work_ex = fields.Char(string="Fisrt work experience ", required=False, )
    tools = fields.Char(string="Tools ", required=False, )
    notice_period = fields.Integer(string="Notice period 'Days' ", required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    candidate_location = fields.Char(string="Candidate Location", required=False, )
    candidate_location_id = fields.Many2one(comodel_name="can.location", string="Candidate Location 1",
                                            required=False, )
    nationality_id = fields.Many2one(comodel_name="nationality", string="Nationality 1", required=False, )
    cv_source = fields.Char(string="CV Source", required=False, )
    current_salary = fields.Float(string="Current Salary", required=False, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=False)
    currency_of_id = fields.Many2one('res.currency', string='Currency Offshore', required=False)
    currency_on_id = fields.Many2one('res.currency', string='Currency OnSite', required=False)
    start_date = fields.Date(string="Start Date", required=False, )
    experience_y = fields.Integer(compute="_calculate_experience",
                                  string="Experience Years",
                                  help="experience in our company", store=True)
    experience_m = fields.Integer(compute="_calculate_experience",
                                  string="Experience monthes", store=True)
    experience_d = fields.Integer(compute="_calculate_experience",
                                  string="Experience dayes", store=True)
    notice_period_to = fields.Integer(string="Notice Period To", required=False, )
    notice_period_from = fields.Integer(string="Notice Period From", required=False, )

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stage_date = dt_string

    def action_activities(self):
        return {
            'name': 'Activities',
            'view_mode': 'calendar,tree,form',
            'res_model': 'mail.activity',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.id)],

        }

    @api.depends('job_id')
    def _compute_stage(self):
        for applicant in self:
            # if applicant.job_id:
            #     if not applicant.stage_id:
            #         stage_ids = self.env['hr.recruitment.stage'].search([
            #             '|',
            #             ('job_ids', '=', False),
            #             ('job_ids', '=', applicant.job_id.id),
            #             ('fold', '=', False)
            #         ], order='sequence asc', limit=1).ids
            #         applicant.stage_id = stage_ids[0] if stage_ids else False
            # else:
            applicant.stage_id = False

    @api.depends("start_date")
    def _calculate_experience(self):
        for app in self.search([]):
            if app.start_date:
                date_format = '%Y-%m-%d'
                current_date = (datetime.today()).strftime(date_format)
                d1 = app.start_date
                d2 = datetime.strptime(current_date, date_format).date()
                r = relativedelta(d2, d1)
                app.experience_y = r.years
                app.experience_m = r.months
                app.experience_d = r.days
            else:
                app.experience_y = 0
                app.experience_m = 0
                app.experience_d = 0

    @api.onchange('partner_mobile', 'partner_phone', 'linkedin', 'email_from', 'job_id', 'email_cc')
    def _onchange_fields(self):
        appliations = self.search([('job_id', '=', self.job_id.id), ('id', '!=', self.id)])
        for app in appliations:
            if self.partner_mobile:
                if app.partner_mobile == self.partner_mobile or app.partner_phone == self.partner_mobile:
                    raise ValidationError("Mobile is Duplicated")
            if self.partner_phone:
                if app.partner_phone == self.partner_phone or app.partner_mobile == self.partner_phone:
                    raise ValidationError("Phone is Duplicated")

            if self.linkedin:
                if app.linkedin == self.linkedin:
                    raise ValidationError("Linkedin is Duplicated")

            if self.email_cc:
                if app.email_cc == self.email_cc or app.email_from == self.email_cc:
                    raise ValidationError("Email CC is Duplicated")
            if self.email_from:
                if app.email_cc == self.email_from or app.email_from == self.email_from:
                    raise ValidationError("Email is Duplicated")


class TypeJob(models.Model):
    _name = 'type.job'

    name = fields.Char('Name')
    activity_ids = fields.One2many('activity.job', 'type_id')


class ActivityJob(models.Model):
    _name = 'activity.job'

    name = fields.Char('Name')
    no_days = fields.Integer('No.days form today')
    type_id = fields.Many2one('type.job')


class nationality(models.Model):
    _name = 'nationality'

    name = fields.Char('Name')


class Canlocation(models.Model):
    _name = 'can.location'

    name = fields.Char('Name')


class JobLang(models.Model):
    _name = 'job.lang'

    name = fields.Char('Name')
