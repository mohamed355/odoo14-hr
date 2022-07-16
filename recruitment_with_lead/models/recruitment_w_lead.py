# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo import models, fields, api, _
from datetime import timedelta, date
class Stage(models.Model):
    _inherit = 'hr.recruitment.stage'

    is_active_state = fields.Boolean(string="Active State")

class HrApp(models.Model):
    _inherit = 'hr.applicant'

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    language_ids = fields.Many2many('job.lang')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female')
    ], string='Gender')
    hiring_id = fields.Many2one(comodel_name="hiring.request", string="hiring", required=False, )
    experience_level = fields.Selection([
        ('intern', 'Intern'), ('fresh', 'Fresh'), ('jr', 'Junior'), ('senior', 'Senior'), ('teamlead', 'Team Lead'),
        ('manager', 'Manager'), ('consultant', 'Consultant')
    ], string='Experience level')
    in_active_state = fields.Boolean(related='stage_id.is_active_state')
    linkedin = fields.Char(string="Linkedin", required=False, )
    first_work_ex = fields.Char(string="Fisrt work experience ", required=False, )
    tools = fields.Char(string="Tools ", required=False, )
    notice_period = fields.Integer(string="Notice period 'Days' ", required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    candidate_location = fields.Char(string="Candidate Location", required=False, )
    cv_source = fields.Char(string="CV Source", required=False, )
    current_salary = fields.Float(string="Current Salary",  required=False, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Recruiter", required=False, )


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


