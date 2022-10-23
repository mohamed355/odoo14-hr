# -*- coding: utf-8 -*-
from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class NewModule(models.TransientModel):
    _name = 'hiring.wizard'
    _description = 'Hiring Wizard'

    req_owner = fields.Char(string="Request Owner", required=False, )
    offered = fields.Integer(string="Offered", required=False, )
    awaiting_review = fields.Integer(string="Awaiting Review", required=False, )
    new_opp = fields.Integer(string="New Applicants", required=False, )
    reviewed = fields.Integer(string="Reviewed", required=False, )
    stage_id = fields.Many2one(comodel_name="hiring.stage", store=True, copy=False, index=True, ondelete='restrict',
                               string="Stage", required=False, group_expand='_read_group_stage_ids')
    hiring = fields.Char(string="Hiring", required=False, )
    av_status = fields.Selection(string="Availability Status",
                                 selection=[('in', 'Interested'), ('not_in', 'Not Interested'), ], required=False, )
    # key_ids = fields.Many2many(comodel_name="key", relation="svg", column1="sdf", column2="fdfd", string="Specific Key Words", )
    job_des = fields.Text(string="Job Requirements And Duties", required=False, )
    impo_level = fields.Selection(string="Importance Level",
                                  selection=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], required=False, )
    # approved = fields.Boolean(string="Approved", )
    # user_ids = fields.Many2many(comodel_name="res.users", relation="resusers", column1="res", column2="users",
    #                             string="Users", )
    tec_ids = fields.Many2many(comodel_name="tec", relation="er", column1="qwe", column2="qwed",
                               string="Required Technology", )
    # name = fields.Char(string='Serial', readonly=True, default="New", track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency')
    requested = fields.Integer(string="Requested", required=False, )
    job_level = fields.Selection(string="Job Level",
                                 selection=[('intern', 'Intern'), ('fresh', 'Fresh'), ('jr', 'Junior'),
                                            ('senior', 'Senior'), ('teamlead', 'Team Lead'), ('manager', 'Manager'),
                                            ('consultant', 'Consultant')], required=False, )
    req_state = fields.Selection(string="Request State",
                                 selection=[('open', 'Open'), ('pending', 'Pending'), ('onhold', 'On Hold'),
                                            ('canceled', 'Canceled'), ('closed', 'Closed')], required=False, )
    budget = fields.Float(string="Budget", required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    note = fields.Text(string="Recruiter Notes", required=False, )
    attach = fields.Binary(string="Attach", )
    location = fields.Char(string="Location", required=True, )
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                string='Appreciation')
    # customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", readonly=True,required=True)
    # client = fields.Many2one(comodel_name="res.partner", string="Client", required=True)
    # customer_address_email = fields.Char('Email', related='customer_id.email', readonly=True)
    # customer_address_phone = fields.Char('Phone', related='customer_id.phone', readonly=True)
    # customer_address_mobile = fields.Char('Mobile', related='customer_id.mobile', readonly=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Salesperson", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", readonly=True)
    comment = fields.Text(string="Other Comments", required=False, )
    tag_ids = fields.Many2many(comodel_name="crm.tag", string="Tags", )
    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=True, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ('any', 'Any')],
                              required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    customer_ids = fields.One2many(comodel_name="hiring.customer", inverse_name="hiring_id", string="Customer",
                                   required=False, )

    partner_id = fields.Many2one(comodel_name="res.partner", required=True, )
    l_1_id = fields.Many2one(comodel_name="res.partner", string="Parent Company", )
    l_3_id = fields.Many2one(comodel_name="res.partner", string="Parent Department", )
    level_2_id = fields.Many2one(comodel_name="res.partner", string="Sector", )
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", )
    level_2_child = fields.One2many(comodel_name="res.partner", related="level_2_id.child_ids", required=True, )
    level_3_child = fields.One2many(comodel_name="res.partner", related="l_3_id.child_ids", required=True, )
    dep_child = fields.One2many(comodel_name="res.partner", related="partner_id.child_ids", required=True, )
    customer_child = fields.One2many(comodel_name="res.partner", related="l_1_id.child_ids", required=True, )

    language_ids = fields.Many2many(comodel_name="job.lang", string="Languages", required=True)
    # department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job = fields.Selection(string='Type Of Job', required=True,
                                   selection=[('eg', 'Contract Eg'), ('ksa', 'Contract Ksa'), ('visit', 'Visit'),
                                              ('iqama', 'Iqama Transfer')], )

    def create_hiring_request(self):
        print('hi')
        for rec in self:
            oppr = self.env['crm.lead'].browse(rec.oppr_id.id)
            Deal = self.env['hiring.request'].create({
                # 'name': 'Hiring Request',
                'oppr_id': oppr.id,
                'nationality': rec.nationality,
                'requested': rec.requested,
                'av_status': rec.av_status,
                'budget': rec.budget,
                'ex_level': rec.ex_level,
                'budget': rec.budget,
                'currency_id': rec.currency_id.id,
                'req_owner': rec.req_owner,
                'user_id': rec.user_id.id,
                'type_of_job': rec.type_of_job,
                'salary_range': rec.salary_range,
                'required_tech': rec.required_tech,
                'required_no': rec.required_no,
                # 'priority': oppr.priority,
                'team_id': rec.team_id.id,
                'tag_ids': rec.tag_ids.ids,
                'country_id': rec.country_id.id,
                'job_id': rec.job_id.id,
                'job_level': rec.job_level,
                'gender': rec.gender,
                'ex_level': rec.ex_level,
                'language_ids': rec.language_ids.ids,
                'tec_ids': rec.tec_ids.ids,
                'job_des': rec.job_des,
                'customer_ids': [(0, 0, {
                    'l_1_id': rec.l_1_id.id,
                    'partner_id': rec.partner_id.id,
                    'l_3_id': rec.l_3_id.id,
                    'contact_id': rec.contact_id.id,
                    'level_2_id': rec.level_2_id.id,
                })],
                'impo_level': rec.impo_level,
                # 'department_id': rec.department_id.id,
                'required_no': rec.required_no,
                'required_tech': rec.required_tech,
                'location': rec.location,
                # 'client': rec.client.id,
                'salary_range': rec.salary_range,
                'type_of_job': rec.type_of_job,
            })


class HiringRequest(models.Model):
    _name = 'hiring.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    req_owner = fields.Char(string="Request Owner", required=False, )
    acc_date = fields.Date(string="Accepted Date", required=False, )
    req_date = fields.Date(string="Request Date", required=False, )
    approve_date = fields.Datetime(string="Approve Date", required=False, )
    offered = fields.Integer(string="Submitted to client", required=False, compute='_compute_application_ids_stages')
    awaiting_review = fields.Integer(string="Approved from client", required=False,
                                     compute='_compute_application_ids_stages')
    new_opp = fields.Integer(string="Accepted technical", required=False, compute='_compute_application_ids_stages')
    reviewed = fields.Integer(string="Offer Accepted", required=False, compute='_compute_application_ids_stages')
    stage_id = fields.Many2one(comodel_name="hiring.stage", store=True, copy=False, index=True, ondelete='restrict',
                               string="Stage", required=False, group_expand='_read_group_stage_ids')
    hiring = fields.Char(string="Hiring", required=False, )
    av_status = fields.Selection(string="Availability Status",
                                 selection=[('in', 'Interested'), ('not_in', 'Not Interested'), ], required=False, )
    # key_ids = fields.Many2many(comodel_name="key", relation="svg", column1="sdf", column2="fdfd", string="Specific Key Words", )
    job_des = fields.Text(string="Job Requirements And Duties", required=False, )
    impo_level = fields.Selection(string="Importance Level",
                                  selection=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], required=False, )
    approved = fields.Boolean(string="Approved", )
    user_ids_real = fields.Many2many(comodel_name="res.users", relation="resuserasds", column1="ssad",
                                     column2="fasfsadsad", string="Users", )
    user_ids = fields.Many2many(comodel_name="res.users", relation="resusers", column1="res", column2="users",
                                string="Users", )
    tec_ids = fields.Many2many(comodel_name="tec", relation="dewf", column1="wf", column2="tfeec",
                               string="Required Technology", )
    name = fields.Char(string='Code', readonly=False, default="New", track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency')
    requested = fields.Integer(string="Requested", required=False, )
    job_level = fields.Selection(string="Job Level",
                                 selection=[('intern', 'Intern'), ('fresh', 'Fresh'), ('jr', 'Junior'),
                                            ('senior', 'Senior'), ('teamlead', 'Team Lead'), ('manager', 'Manager'),
                                            ('consultant', 'Consultant')], required=False, )
    req_state = fields.Selection(string="Request State",
                                 selection=[('open', 'Open'), ('pending', 'Pending'), ('onhold', 'On Hold'),
                                            ('canceled', 'Canceled'), ('closed', 'Closed')], required=False, )
    budget = fields.Float(string="Budget", required=False, )
    nationality = fields.Char(string="Nationality", required=False, )
    note = fields.Text(string="Recruiter Notes", required=False, )
    attach = fields.Binary(string="Attach", )
    location = fields.Char(string="Location", required=True, )
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                string='Appreciation')
    # customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", readonly=True,required=True)
    # client = fields.Many2one(comodel_name="res.partner", string="Client", required=True)
    # customer_address_email = fields.Char('Email', related='customer_id.email', readonly=True)
    # customer_address_phone = fields.Char('Phone', related='customer_id.phone', readonly=True)
    # customer_address_mobile = fields.Char('Mobile', related='customer_id.mobile', readonly=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Salesperson", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", readonly=True)
    comment = fields.Text(string="Other Comments", required=False, )
    tag_ids = fields.Many2many(comodel_name="crm.tag", string="Tags", readonly=False)
    oppr_id = fields.Many2one(comodel_name="crm.lead", string="Oppr", required=False)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job", required=True, )
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ('any', 'Any')],
                              required=False, )
    ex_level = fields.Selection(string="Experience level", selection=[('f', 'Fundamental Awareness'), ('n', 'Novice'),
                                                                      ('i', 'Intermediate'), ('a', 'Advanced'),
                                                                      ('e', 'Expert')], required=False, )
    customer_ids = fields.One2many(comodel_name="hiring.customer", inverse_name="hiring_id", string="Customer",
                                   required=False, )
    language_ids = fields.Many2many(comodel_name="job.lang", string="Languages", required=True)
    # department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    required_no = fields.Integer(string='Number of Required Employees')
    required_tech = fields.Char(string='Required Technology')
    salary_range = fields.Char(string='Salary Range')
    type_of_job = fields.Selection(string='Type Of Job', required=True,
                                   selection=[('eg', 'Contract Eg'), ('ksa', 'Contract Ksa'), ('visit', 'Visit'),
                                              ('iqama', 'Iqama Transfer')], )
    app_count = fields.Integer(compute='_compute_application_ids', string="Number of applications")
    # active_count = fields.Integer(compute='_compute_activity_count', string="Number of applications")
    application_ids = fields.Many2many(comodel_name="hr.applicant", relation="hr_application_rel",
                                       column1='application_id', column2="hr_id", string="Application")
    activity_count = fields.Integer(string="Activities", required=False, compute='_compute_activity_count')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'hiring.req.code')
        vals['req_date'] = fields.Datetime.now()
        return super(HiringRequest, self).create(vals)

    @api.depends('application_ids')
    def _compute_application_ids_stages(self):
        for record in self:
            record.offered = self.env['hr.applicant'].search_count(
                [('id', 'in', record.application_ids.ids), ('stage_id.name', '=', "Submitted to client")])
            record.reviewed = self.env['hr.applicant'].search_count(
                [('id', 'in', record.application_ids.ids), ('stage_id.name', '=', "Offer Accepted")])
            record.new_opp = self.env['hr.applicant'].search_count(
                [('id', 'in', record.application_ids.ids), ('stage_id.name', '=', "Accepted technical")])
            record.awaiting_review = self.env['hr.applicant'].search_count(
                [('id', 'in', record.application_ids.ids), ('stage_id.name', '=', "Approved from client")])

    def create_application(self):
        application = self.env['hr.applicant'].create({
            'name': "Application from hiring",
            'experience_level': self.job_level,
            # 'country_id':self.country_id.id,
            'language_ids': self.language_ids.ids,
            'gender': self.gender,
            'job_id': self.job_id.id,
            'nationality': self.nationality,
            # 'department_id': self.department_id.id,
            'hiring_id': self.id,
        })

    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['hiring.stage'].search([], order='sequence asc')

    def approve(self):
        self.approved = True

    @api.depends()
    def _compute_application_ids(self):
        for rec in self:
            if rec.application_ids:
                rec.app_count = len(rec.application_ids)
            else:
                rec.app_count = 0

    def create_activities(self):
        print('hi')
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

    def _compute_activity_count(self):
        for record in self:
            if record.application_ids:
                record.activity_count = self.env['mail.activity'].sudo().search_count(
                    [('res_model_id.model', '=', 'hr.applicant'), ('res_id', 'in', self.application_ids.ids)])
            else:
                record.activity_count = 0

    def get_activities(self):
        form_view = self.env.ref('mail.mail_activity_view_form_popup').id
        tree_view = self.env.ref('mail.mail_activity_view_tree').id
        return {
            'name': _('Activities'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'mail.activity',
            'type': 'ir.actions.act_window',
            'views': [
                (tree_view, 'tree'),
                (form_view, 'form'),
            ],
            'domain': [('res_model_id.model', '=', 'hr.applicant'), ('res_id', 'in', self.application_ids.ids)],
        }

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

    # def _compute_activity_count(self):
    #     for product in self:
    #         product.active_count = self.env['mail.activity'].sudo().search_count(
    #             [('res_model_id', '=', product._name), ('res_id', '=', product.id)])


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

    def open_hiring_request(self):
        return {
            'name': 'Hiring Wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hiring.wizard',
            'type': 'ir.actions.act_window',
            'context': {
                'default_l_1_id': self.l_1_id.id,
                'default_l_3_id': self.l_3_id.id,
                'default_level_2_id': self.level_2_id.id,
                'default_contact_id': self.contact_id.id,
                'default_partner_id': self.partner_id.id,
            },
            'target': 'new'

        }

    def compute_hiring_requests(self):
        for rec in self:
            rec.hiring_requests_count = len(self.env['hiring.request'].search([('oppr_id', '=', rec.id)]))


class HiringRequestCustomer(models.Model):
    _name = 'hiring.customer'

    email = fields.Char(string="Email", required=False, )
    mobile = fields.Char(string="Mobile", required=False, )
    partner_id = fields.Many2one(string="Section", comodel_name="res.partner", required=False, )
    l_1_id = fields.Many2one(comodel_name="res.partner", string="Parent Company", )
    l_3_id = fields.Many2one(comodel_name="res.partner", string="Parent Department", )
    level_2_id = fields.Many2one(comodel_name="res.partner", string="Department", )
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", )
    level_2_child = fields.One2many(comodel_name="res.partner", related="level_2_id.child_ids", required=False, )
    level_3_child = fields.One2many(comodel_name="res.partner", related="l_3_id.child_ids", required=False, )
    dep_child = fields.One2many(comodel_name="res.partner", related="partner_id.child_ids", required=False, )
    customer_child = fields.One2many(comodel_name="res.partner", related="l_1_id.child_ids", required=False, )
    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", required=False, )

    @api.onchange('contact_id')
    def onchange_email(self):
        self.email = self.contact_id.email
        self.mobile = self.contact_id.mobile


class key(models.Model):
    _name = 'key'
    color = fields.Integer('Color Index', default=0)

    name = fields.Char()


class CrmTag(models.Model):
    _name = 'crm.tag'

    color = fields.Integer('Color Index', default=0)
    name = fields.Char()


class tec(models.Model):
    _name = 'tec'
    color = fields.Integer('Color Index', default=0)

    name = fields.Char()


class stage(models.Model):
    _name = 'hiring.stage'
    _order = 'sequence asc'

    name = fields.Char()
    sequence = fields.Integer("Sequence")
    # handle = fields.Integer("Handle")


class HrApplication(models.Model):
    _inherit = 'hr.applicant'
    _rec_name = "partner_name"
    acc_date = fields.Date(string="Accepted Date", required=False, )

    def name_get(self):
        result = []

        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.partner_name, rec.app_code)))

        return result

    hiring_ids = fields.Many2many(comodel_name="hiring.request", relation="asd", column1="df", column2="das",
                                  string="Hiring", store=True)


class AssignApplications(models.Model):
    _name = 'assign.application'

    name = fields.Char(default="Assign Applications")
    applications_ids = fields.Many2many(comodel_name="hr.applicant", relation="hrapplicant", column1="hr",
                                        column2="applicant", string="Applications", )

    def assign_applications(self):
        hiring = self.env['hiring.request'].browse(self.env.context.get('active_id'))
        apps_exist = []
        for application in self.applications_ids:
            if application.id in hiring.application_ids.ids:
                apps_exist.append(application.name)

            else:
                hiring.update({'application_ids': [(4, application.id)]})
                # application.update({'hiring_ids': [(4, hiring.id)]})
                application.approve_date = fields.Datetime.now()

        if apps_exist:
            raise ValidationError('This Applications %s Already Assigned ' % apps_exist)
