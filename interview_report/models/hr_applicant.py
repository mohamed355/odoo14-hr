from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.onchange('inter_by', 'interview_date')
    def _onchange_inter_by(self):
        if self.inter_by and self.interview_date:
            app = self.env['hr.applicant'].search([('partner_name', '=', self.partner_name)])
            interview = self.env['interview.report'].create({
                'name': self.app_code,
                'location': self.location,
                'mobile': self.partner_mobile,
                'email': self.email_from,
                'job_id': self.job_id.id,
                'interviewed_by': self.inter_by,
                'date': self.interview_date,
                'app_name': self.partner_name,
            })
            if self.refuse_reason_id:
                interview.write({'re_reason': self.refuse_reason_id.name})
            att = self.env['ir.attachment'].search([('res_id', '=', app.id), ('res_model', '=', 'hr.applicant')])
            print(att, "ATT")
            if att:
                interview.write({'resume': att.datas})
                interview.write({'att': att.id})
