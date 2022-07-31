from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrDashboard(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def get_data(self):
        hr_applicant=self.env['hr.applicant'].search([])
        open_hiring=self.env['hiring.request'].search([])

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

    @api.model
    def get_job(self):
        stages = self.env['hr.recruitment.stage'].search([])
        stages_list = []
        for record in stages:
            print(record)
            stages_of_apps = self.env['hr.applicant'].search_count([('stage_id', '=', record.id)])
            record_list = list(record)
            record_list.append(record.name)
            record_list.append(record.num_of_apps)
            record_list.append(stages_of_apps)
            stages_list.append(record_list)
            print(record_list)
        print("stages_list", stages_list)
        return {'stages_list': stages_list}

    @api.model
    def get_recruiter(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,res_partner.name as partner from 
        hr_applicant inner join res_partner on 
        res_partner.id =hr_applicant.partner_id group by partner ORDER BY co DESC'''

        self._cr.execute(query)
        partners = self._cr.dictfetchall()
        total_app = []
        for record in partners:
            # if record.get('total_quantity') != 0:
            #     print(total_quantity.append(record.get('total_quantity')))
            total_app.append(record.get('co'))
        partner_name = []
        for record in partners:
            partner_name.append(record.get('partner'))
        final = [total_app,partner_name]
        return final

    @api.model
    def get_jobs(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hr_job.name as job from 
            hr_applicant inner join hr_job on 
            hr_job.id =hr_applicant.job_id group by job ORDER BY co DESC'''

        self._cr.execute(query)
        jobs = self._cr.dictfetchall()
        total_app = []
        for record in jobs:
            # if record.get('total_quantity') != 0:
            #     print(total_quantity.append(record.get('total_quantity')))
            total_app.append(record.get('co'))
        job_name = []
        for record in jobs:
            job_name.append(record.get('job'))
        final = [total_app, job_name]
        return final

    @api.model
    def get_act_don(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,activity_type as type from 
                mail_activity group by activity_type ORDER BY co DESC'''

        self._cr.execute(query)
        activties = self._cr.dictfetchall()
        total_ac = []
        for record in activties:
            # if record.get('total_quantity') != 0:
            #     print(total_quantity.append(record.get('total_quantity')))
            total_ac.append(record.get('co'))
        stat = []
        for record in activties:
            stat.append(record.get('type'))
        final = [total_ac, stat]
        return final

    @api.model
    def get_sources(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,utm_source.name as source from 
                hr_applicant inner join utm_source on 
                utm_source.id =hr_applicant.source_id group by source ORDER BY co DESC'''

        self._cr.execute(query)
        source = self._cr.dictfetchall()
        total_app = []
        for record in source:
            # if record.get('total_quantity') != 0:
            #     print(total_quantity.append(record.get('total_quantity')))
            total_app.append(record.get('co'))
        source_name = []
        for record in source:
            source_name.append(record.get('source'))
        final = [total_app, source_name]
        return final