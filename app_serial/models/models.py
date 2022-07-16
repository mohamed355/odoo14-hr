# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrApp(models.Model):
    _inherit = 'hr.applicant'


    app_code = fields.Char(string="Serial", required=False )
    short_code = fields.Char(string="Short Code", required=False )
    code = fields.Char(string="code", required=False )

    @api.model
    def create(self, vals):
        if vals['code']:
            vals['app_code'] =  self.env['ir.sequence'].next_by_code(
                vals['code'])
        return super(HrApp, self).create(vals)

    @api.onchange('job_id')
    def onchange_job_id(self):
        self.short_code = self.job_id.short_code
        self.code = self.job_id.seq_code

class HrJob(models.Model):
    _inherit = 'hr.job'

    short_code = fields.Char(string="Short Code", required=False, )
    seq_code = fields.Char(string="Seq Code", required=False, )


class CreateSeq(models.Model):
    _name = 'create.seq'

    name = fields.Char(default="Create Seq")
    name_seq = fields.Char(string="Sequence Name" ,required=True)
    prefix = fields.Char(string="Prefix", required=True, )
    code = fields.Char(string="Code", required=True, )
    padding = fields.Char(string="Padding", required=True, )


    def create_seq(self):
        seq = self.env['ir.sequence'].create({
            'code':self.code,
            'name':self.name_seq,
            'prefix':self.prefix,
            'padding':self.padding,
        })
        job = self.env['hr.job'].browse(self._context.get('active_id'))
        job.short_code = seq.prefix
        job.seq_code = seq.code

    @api.onchange('prefix')
    def onchange_prefix(self):
        if self.prefix:
            self.name_seq = self.prefix + " Seq"

    @api.onchange('name_seq')
    def onchange_name_seq(self):
        if self.name_seq:
            code = self.name_seq.lower()
            code = code.replace(" " , ".")
            self.code = code
