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
    experience_level = fields.Selection([
        ('f', ' Fundamental Awareness'),
        ('n', 'Novice'),
        ('i', 'Intermediate'),
        ('a', 'Advanced'),
        ('e', 'Expert')
    ], string='Experience level')
    in_active_state = fields.Boolean(related='stage_id.is_active_state')


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

