# -*- coding: utf-8 -*-
from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class NewModule(models.TransientModel):
    _name = 'hiring.wizard'
    _description = 'Hiring Wizard'

    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=False, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    language_ids = fields.Many2many(comodel_name="job.lang", string="Language", required=False)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job_id = fields.Many2one(comodel_name="type.job", string="Type Of Job", required=False)

    def create_hiring_request(self):
        print('hi')
        for rec in self:
            oppr = self.env['crm.lead'].browse(rec.oppr_id.id)
            Deal = self.env['hiring.request'].create({
                    'name': 'Hiring Request',
                    'oppr_id': oppr.id,
                    'customer_id': oppr.partner_id.id,
                    'customer_address_email': oppr.partner_id.email,
                    'customer_address_phone': oppr.partner_id.phone,
                    'customer_address_mobile': oppr.partner_id.mobile,
                    'user_id': oppr.user_id.id,
                    'team_id': oppr.team_id.id,
                    'tag_ids': oppr.tag_ids.ids,
                    'country_id': rec.country_id.id,
                    'job_id': rec.job_id.id,
                    'gender': rec.gender,
                    'ex_level': rec.ex_level,
                    'language_ids': rec.language_ids.ids,
                    'department_id': rec.department_id.id,
                    'required_no': rec.required_no,
                    'required_tech': rec.required_tech,
                    'salary_range': rec.salary_range,
                    'type_of_job': rec.type_of_job_id.id,
                })


class HiringRequest(models.Model):
    _name = 'hiring.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", readonly=True)
    customer_address_email = fields.Char('Email', related='customer_id.email', readonly=True)
    customer_address_phone = fields.Char('Phone', related='customer_id.phone', readonly=True)
    customer_address_mobile = fields.Char('Mobile', related='customer_id.mobile', readonly=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Salesperson", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", readonly=True)
    tag_ids = fields.Many2many(comodel_name="crm.tag", string="Tags", readonly=True)
    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=False, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    language_ids = fields.Many2many(comodel_name="job.lang", string="Languages", required=False)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job = fields.Many2one('type.job', string='Type Of Job')
    app_count = fields.Integer(compute='_compute_app_count', string="Number of applications")
    active_count = fields.Integer(compute='_compute_activity_count', string="Number of applications")

    def create_activities(self):
        print('hi')
        if self.type_of_job and self.type_of_job.activity_ids:
            for i in self.type_of_job.activity_ids:
                self.env['mail.activity'].sudo().create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'note': i.name,
                    'user_id': self._uid,
                    'res_id': self.id,
                    'date_deadline': date.today() + timedelta(days=i.no_days),
                    'res_model_id': self.env['ir.model'].sudo().search(
                         [('model', '=', 'hiring.request')], limit=1).id,
                })
        else:
            raise ValidationError("Please add type of job and activities")

    def application_no(self):
        self.ensure_one()
        action = {
            'name': _('Application Requests'),
            'view_type': 'form',
            'view_mode': 'kanban,tree,form,pivot,graph,calendar',
            'res_model': 'hr.applicant',
            'type': 'ir.actions.act_window',
            'domain': [('country_id', '=', self.country_id.id), ('job_id', '=', self.job_id.id),
                       ('gender', '=', self.gender), ('experience_level', '=', self.ex_level),
                       ('in_active_state', '=', True)],
        }

        return action

    def activity_no(self):
        self.ensure_one()
        action = {
            'name': _('Activity Requests'),
            'view_type': 'form',
            'view_mode': 'tree,form,pivot,graph,calendar',
            'res_model': 'mail.activity',
            'type': 'ir.actions.act_window',
            'domain': [('res_model_id', '=', self._name), ('res_id', '=', self.id)],
        }

        return action


    def _compute_app_count(self):
        for product in self:
            product.app_count = self.env['hr.applicant'].search_count(
                [('country_id', '=', self.country_id.id), ('job_id', '=', self.job_id.id), ('gender', '=', self.gender),
                 ('experience_level', '=', self.ex_level), ('in_active_state', '=', True)])


    def _compute_activity_count(self):
        for product in self:
            product.active_count = self.env['mail.activity'].sudo().search_count(
                [('res_model_id', '=', product._name), ('res_id', '=', product.id)])


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    hiring_requests_count = fields.Integer(compute='compute_hiring_requests')

    def get_hiring_requests(self):
        self.ensure_one()
        tree_view = self.env.ref('rawafd_hiring_request.hiring_request_tree').id
        form_view = self.env.ref('rawafd_hiring_request.hiring_request_form').id
        return {
            'name': 'Hiring Requests',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'hiring.request',
            'view_id': False,
            'views': [(tree_view, 'tree'), (form_view, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('oppr_id', '=', self.id)],
        }


    def compute_hiring_requests(self):
        for rec in self:
            rec.hiring_requests_count = len(self.env['hiring.request'].search([('oppr_id', '=', rec.id)]))




