# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'hr.applicant'

    @api.depends('task_checklist')
    def checklist_progress(self):
        total_len = self.env['task.checklist'].search_count([])
        for rec in self:
            if total_len != 0:
                check_list_len = len(rec.task_checklist)
                rec.checklist_progress = (check_list_len * 100) / total_len
            else:
                rec.checklist_progress = 0

    task_checklist = fields.Many2many('task.checklist', string='Check List')
    checklist_progress = fields.Float(compute=checklist_progress, string='Progress', store=True,
                                      default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)
    reviewed_by_id = fields.Many2one(comodel_name="res.users", string="Reviewed By", required=False, )

    @api.constrains('stage_id')
    def constrains_stage_id_checklist(self):
        if self.stage_id.name == 'Submit to client':
            if not self.reviewed_by_id:
                raise ValidationError("Please Select Reviewed By")


class TaskChecklist(models.Model):
    _name = 'task.checklist'
    _description = 'Checklist for the task'
    _order = 'sequence asc'

    sequence = fields.Integer("Sequence")
    name = fields.Char(string='Name', required=False)
    description = fields.Char(string='Description')
