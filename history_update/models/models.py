# -*- coding: utf-8 -*-
from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HiringRequest(models.Model):
    _inherit = 'hiring.request'

    user_ids = fields.One2many(comodel_name="user.history", inverse_name="hiring_id", string="Users", required=False, )
    admin = fields.Boolean(string="Admin", compute='_compute_admin')

    @api.depends()
    def _compute_admin(self):
        for record in self:
            if self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
                record.admin = True
            else:
                record.admin = False


class HrApplication(models.Model):
    _inherit = 'hr.applicant'
    _rec_name = "partner_name"

    name = fields.Char("Subject / Application Name", required=False,
                       help="Email subject for applications sent via email")
    approve_date = fields.Datetime(string="Approve Date", required=False, )
    hiring_ids = fields.Many2many(comodel_name="hiring.request", relation="asd", column1="df", column2="das",
                                  string="Hiring", store=True)
    rej_boolean = fields.Boolean("rejected or no feedback")
    # admin = fields.Boolean(string="Admin", compute='_compute_admin')
    #
    # @api.depends()
    # def _compute_admin(self):
    #     for record in self:
    #         if self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
    #             record.admin = True
    #         else:
    #             record.admin = False


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
            if application.hiring_ids:
                raise ValidationError('This Applications Already In Hiring Request ')
            else:
                hiring.update({'application_ids': [(4, application.id)]})
                application.update({'hiring_ids': [(4, hiring.id)]})
                # application.hiring_id =  hiring.id
                application.approve_date = fields.Datetime.now()

        if apps_exist:
            raise ValidationError('This Applications %s Already Assigned ' % apps_exist)


class usershistory(models.Model):
    _name = 'user.history'

    hiring_id = fields.Many2one(comodel_name="hiring.request", string="Hiring", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="User", required=False, )
    start_date = fields.Datetime(string="Start Date", required=False, )
    end_date = fields.Datetime(string="End Date", required=False, )
    duration = fields.Integer(string="Duration", required=False, compute='_compute_duration')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = abs(record.start_date - record.end_date).days
            else:
                record.duration = 0


class AssignUsers(models.TransientModel):
    _name = 'assign.users'

    user_ids = fields.Many2many(comodel_name="res.users", relation="resusersdasf", column1="resafduser",
                                column2="afasasafasfas", string="Users", )

    def assign_users(self):
        hiring = self.env['hiring.request'].browse(self.env.context.get('active_id'))
        hiring.approved = True
        hiring.acc_date = fields.Date.today()
        for user in self.user_ids:
            self.env['user.history'].create({
                'user_id': user.id,
                'start_date': fields.Datetime.today(),
                'hiring_id': hiring.id,
            })
            hiring.update({'user_ids_real': [(4, user.id)]})


class UnAssignUsers(models.TransientModel):
    _name = 'unassign.users'

    user_ids = fields.Many2many(comodel_name="res.users", relation="asdff", column1="dafdf", column2="sddf",
                                string="Users", )

    def unassign_users(self):
        hiring = self.env['hiring.request'].browse(self.env.context.get('active_id'))
        hiring.approved = True
        print("Hiring")
        hiring.acc_date = fields.Date.today()
        for user in self.user_ids:
            user_s = self.env['user.history'].search(
                [('user_id', '=', user.id), ('end_date', '=', False), ('hiring_id', '=', hiring.id)])
            if user_s:
                user_s.end_date = fields.Datetime.today()
            hiring.update({'user_ids_real': [(3, user.id, False)]})
