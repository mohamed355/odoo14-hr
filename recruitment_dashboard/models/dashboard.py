from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrDashboard(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def get_data(self):
        hr_applicant=self.env['hr.applicant'].search([])
        open_hiring=self.env['hiring.request'].search([('req_state','!=','closed')])

        return {
            'open_hiring':len(open_hiring),
            'hr_applicant':len(hr_applicant),
            # 'stages':stages

        }

    @api.model
    def get_stages(self):
        """Recent Activities Table"""
        stages=self.env['hr.recruitment.stage'].search([])
        stages_list = []
        for record in stages:
            print(record)
            stages_of_apps = self.env['hr.applicant'].search_count([('stage_id','=',record.id)])
            record_list = list(record)
            record_list.append(record.name)
            record_list.append(record.num_of_apps)
            record_list.append(stages_of_apps)
            stages_list.append(record_list)
            print(record_list)
        print("stages_list", stages_list)
        return {'stages_list': stages_list}
