# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo import models, fields, api, _
from datetime import timedelta, date,datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime

# class Stage(models.Model):
#     _inherit = 'hr.recruitment.stage'
#
#     is_active_state = fields.Boolean(string="Active State")


class HrApp(models.Model):
    _inherit = 'hr.applicant'

    ex_of = fields.Float(string="Expected(Offshore)",  required=False, )
    ex_on = fields.Float(string="Expected(Onsite)",  required=False, )
    current_salary = fields.Float(string="Current Salary",  required=False, )
    stage_date = fields.Datetime(string="Stage Time", required=False, )
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    language_ids = fields.Many2many('job.lang')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender')
    # hiring_id = fields.Many2one(comodel_name="hiring.request", string="hiring", required=False, )
    experience_level = fields.Selection([
        ('intern', 'Intern'), ('fresh', 'Fresh'), ('jr', 'Junior'), ('senior', 'Senior'), ('teamlead', 'Team Lead'),
        ('manager', 'Manager'), ('consultant', 'Consultant')
    ], string='Experience level')
    # in_active_state = fields.Boolean(related='stage_id.is_active_state')
    linkedin = fields.Char(string="Linkedin", required=False, )
    first_work_ex = fields.Char(string="Fisrt work experience ", required=False, )
    tools = fields.Char(string="Tools ", required=False, )
    notice_period = fields.Integer(string="Notice period 'Days' ", required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    candidate_location = fields.Char(string="Candidate Location", required=False, )
    cv_source = fields.Char(string="CV Source", required=False, )
    current_salary = fields.Float(string="Current Salary",  required=False, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=False)
    currency_of_id = fields.Many2one('res.currency', string='Currency', required=False)
    currency_on_id = fields.Many2one('res.currency', string='Currency', required=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Recruiter", required=False, )
    start_date = fields.Date(string="Start Date", required=False, )
    experience_y = fields.Integer(compute="_calculate_experience",
                                  string="Experience Years",
                                  help="experience in our company", store=True)
    experience_m = fields.Integer(compute="_calculate_experience",
                                  string="Experience monthes", store=True)
    experience_d = fields.Integer(compute="_calculate_experience",
                                  string="Experience dayes", store=True)

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

    # @api.onchange('partner_mobile','linkedin','email_from')
    # def _onchange_fields(self):
    #     appliations = self.env['hr.applicant'].search([('job_id','=',self.job_id.id)])
    #     for app in applications:
    #         if self.partner_mobile:
    #             if app.partner_mobile == self.partner_mobile:
    #                 raise ValidationError("Mobile is Duplicated")
    #         if self.linkedin:
    #             if app.linkedin == self.linkedin:
    #                 raise ValidationError("Linkedin is Duplicated")
    #
    #         if self.email_from:
    #             if app.email_from == self.email_from:
    #                 raise ValidationError("Email is Duplicated")



class TypeJob(models.Model):
    _name = 'type.job'

    name = fields.Char('Name')
    activity_ids = fields.One2many('activity.job', 'type_id')


class ActivityJob(models.Model):
    _name = 'activity.job'

    name = fields.Char('Name')
    no_days = fields.Integer('No.days form today')
    type_id = fields.Many2one('type.job')


class JobLang(models.Model):
    _name = 'job.lang'

    name = fields.Char('Name')


