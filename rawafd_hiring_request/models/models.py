# -*- coding: utf-8 -*-
from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class NewModule(models.TransientModel):
    _name = 'hiring.wizard'
    _description = 'Hiring Wizard'

    key_ids = fields.Many2many(comodel_name="key", relation="wizkey", column1="wiz", column2="key", string="Specific Key Words", )
    tec_ids = fields.Many2many(comodel_name="tec", relation="wiztec", column1="w", column2="tec", string="Required Technology", )
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Appreciation')
    job_des = fields.Text(string="Job Requirements And Duties", required=False, )
    impo_level = fields.Selection(string="Importance Level",
                                  selection=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], required=False, )

    client = fields.Many2one(comodel_name="res.partner", string="Client",required=True)
    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=False, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    location = fields.Char(string="Location", required=True, )

    language_ids = fields.Many2many(comodel_name="job.lang", string="Language", required=False)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job_id = fields.Selection( string='Type Of Job',required=True, selection=[('eg', 'Contract Eg'), ('ksa', 'Contract Ksa'),('visit', 'Visit'),('iqama', 'Iqama Transfer') ],)
    job_level = fields.Selection(string="Job Level", selection=[('intern', 'Intern'),('fresh', 'Fresh'), ('jr', 'Junior'), ('senior', 'Senior') ,('teamlead', 'Team Lead'),('manager', 'Manager'),('consultant', 'Consultant')], required=False, )

    def create_hiring_request(self):
        print('hi')
        for rec in self:
            oppr = self.env['crm.lead'].browse(rec.oppr_id.id)
            Deal = self.env['hiring.request'].create({
                    # 'name': 'Hiring Request',
                    'oppr_id': oppr.id,
                    # 'customer_id': oppr.partner_id.id,
                    # 'customer_address_email': oppr.partner_id.email,
                    # 'customer_address_phone': oppr.partner_id.phone,
                    # 'customer_address_mobile': oppr.partner_id.mobile,
                    'user_id': oppr.user_id.id,
                    'priority': oppr.priority,
                    'team_id': oppr.team_id.id,
                    'tag_ids': oppr.tag_ids.ids,
                    'country_id': rec.country_id.id,
                    'job_id': rec.job_id.id,
                    'job_level': rec.job_level,
                    'gender': rec.gender,
                    'ex_level': rec.ex_level,
                    'language_ids': rec.language_ids.ids,
                    'key_ids': rec.key_ids.ids,
                    'tec_ids': rec.tec_ids.ids,
                    'job_des': rec.job_des,
                    'impo_level': rec.impo_level,
                    'department_id': rec.department_id.id,
                    'required_no': rec.required_no,
                    'required_tech': rec.required_tech,
                    'location': rec.location,
                    'client': rec.client.id,
                    'salary_range': rec.salary_range,
                    'type_of_job': rec.type_of_job_id,
                })


class HiringRequest(models.Model):
    _name = 'hiring.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # @api.model
    # def _get_default_stage_id(self):
    #     return self.env['hiring.stage'].search([], limit=1)

    stage_id = fields.Many2one(comodel_name="hiring.stage",default=lambda self: self.env['hiring.request'].search([], limit=1),ondelete='restrict',string="Stage",required=False, )
    av_status = fields.Selection(string="Availability Status", selection=[('in', 'Interested'), ('not_in', 'Not Interested'), ], required=False, )
    key_ids = fields.Many2many(comodel_name="key", relation="svg", column1="sdf", column2="fdfd", string="Specific Key Words", )
    job_des = fields.Text(string="Job Requirements And Duties", required=False, )
    impo_level = fields.Selection(string="Importance Level",
                                  selection=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], required=False, )
    tec_ids = fields.Many2many(comodel_name="tec", relation="dewf", column1="wf", column2="tfeec", string="Required Technology", )

    name = fields.Char(string='Serial' ,readonly=True, default="New")
    currency_id = fields.Many2one('res.currency', string='Currency')
    requested = fields.Integer(string="Requested", required=False, )
    job_level = fields.Selection(string="Job Level", selection=[('intern', 'Intern'),('fresh', 'Fresh'), ('jr', 'Junior'), ('senior', 'Senior') ,('teamlead', 'Team Lead'),('manager', 'Manager'),('consultant', 'Consultant')], required=False, )
    req_state = fields.Selection(string="Request State", selection=[('open', 'Open'), ('pending', 'Pending'), ('onhold', 'On Hold'), ('canceled', 'Canceled') , ('closed', 'Closed')], required=False, )
    budget = fields.Float(string="Budget",  required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    note = fields.Text(string="Contact Notes", required=False, )
    attach = fields.Binary(string="Attach",)
    location = fields.Char(string="Location", required=True, )
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Appreciation')
    # customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", readonly=True,required=True)
    client = fields.Many2one(comodel_name="res.partner", string="Client",required=True)
    # customer_address_email = fields.Char('Email', related='customer_id.email', readonly=True)
    # customer_address_phone = fields.Char('Phone', related='customer_id.phone', readonly=True)
    # customer_address_mobile = fields.Char('Mobile', related='customer_id.mobile', readonly=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Salesperson", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", readonly=True)
    comment = fields.Text(string="Other Comments", required=False, )
    tag_ids = fields.Many2many(comodel_name="crm.tag", string="Tags", readonly=True)
    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=True, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    customer_ids = fields.One2many(comodel_name="hiring.customer", inverse_name="hiring_id", string="Customer", required=False, )
    language_ids = fields.Many2many(comodel_name="job.lang", string="Languages", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job = fields.Selection( string='Type Of Job',required=True, selection=[('eg', 'Contract Eg'), ('ksa', 'Contract Ksa'),('visit', 'Visit'),('iqama', 'Iqama Transfer') ],)
    app_count = fields.Integer(compute='_compute_application_ids', string="Number of applications")
    active_count = fields.Integer(compute='_compute_activity_count', string="Number of applications")
    application_ids = fields.Many2many(comodel_name="hr.applicant", relation="hr_application_rel", column1='application_id', column2="hr_id", string="Application")

    def create_application(self):
        application = self.env['hr.applicant'].create({
            'name':"Application from hiring",
            'experience_level':self.job_level,
            'country_id':self.country_id.id,
            'language_ids':self.language_ids.ids,
            'gender':self.gender,
            'job_id':self.job_id.id,
            'nationality':self.nationality,
            'department_id':self.department_id.id,
            'hiring_id':self.id,
        })
    #
    @api.depends()
    def _compute_application_ids(self):
        for rec in self:
            rec.app_count = len(rec.application_ids)
            # rec.application_ids = self.env['hr.applicant'].search([('hiring_id', '=', rec.id)]).ids



    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'hiring.req.code')
        return super(HiringRequest, self).create(vals)

    def create_activities(self):
        print('hi')
        # if self and self.activity_ids:
        for i in self.activity_ids:
            self.env['mail.activity'].sudo().create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': i.name,
                'user_id': self._uid,
                'res_id': self.id,
                'date_deadline': date.today() + timedelta(days=i.no_days),
                'res_model_id': self.env['ir.model'].sudo().search(
                     [('model', '=', 'hiring.request')], limit=1).id,
            })
        # else:
        #     raise ValidationError("Please add type of job and activities")

    def application_no(self):
        self.ensure_one()
        action = {
            'name': _('Application Requests'),
            'view_type': 'form',
            'view_mode': 'kanban,tree,form,pivot,graph,calendar',
            'res_model': 'hr.applicant',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.application_ids.ids)
                       ],
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


    # def _compute_app_count(self):
    #     for product in self:
    #         product.app_count = self.env['hr.applicant'].search_count(
    #             [('country_id', '=', self.country_id.id), ('job_id', '=', self.job_id.id), ])

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


class HiringRequestCustomer(models.Model):
    _name = 'hiring.customer'

    email = fields.Char(string="Email",required=False, )
    mobile = fields.Char(string="Mobile",required=False, )
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer",  )
    level_1_id = fields.Many2one(comodel_name="res.partner", string="Level 1",  )
    level_1_child= fields.One2many(comodel_name="res.partner",related="level_1_id.child_ids", required=True, )
    customer_child= fields.One2many(comodel_name="res.partner",related="customer_id.child_ids", required=True, )
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", )
    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", required=False, )

    @api.onchange('contact_id')
    def onchange_email(self):
        self.email = self.contact_id.email
        self.mobile = self.contact_id.mobile


class key(models.Model):
    _name = 'key'
    color = fields.Integer('Color Index', default=0)

    name = fields.Char()


class tec(models.Model):
    _name = 'tec'
    color = fields.Integer('Color Index', default=0)

    name = fields.Char()


class stage(models.Model):
    _name = 'hiring.stage'

    name = fields.Char()

