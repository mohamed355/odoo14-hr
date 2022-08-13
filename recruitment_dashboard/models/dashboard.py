from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from odoo.tools import date_utils


class HrDashboard(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def get_data(self):
        hr_applicant=self.env['hr.applicant'].search([])
        open_hiring=self.env['hiring.request'].search([])
        com_hiring=self.env['hiring.request'].search_count([("stage_id.name",'=',"Completed")])
        h_a = 0
        if round(len(hr_applicant) / len(open_hiring)):
            h_a = round(len(hr_applicant) / len(open_hiring))
        h_com = 0
        if round(len(hr_applicant) / len(open_hiring)):
            h_com = round(len(open_hiring) / com_hiring)
        return {
            'open_hiring':len(open_hiring),
            'hr_applicant':len(hr_applicant),
            'h_a':h_a,
            'h_com':h_com,

        }

    @api.model
    def crm_year(self):
        """Year CRM Dropdown Filter"""
        # session_user_id = self.env.uid

        self._cr.execute('''select COUNT(id) from hr_applicant WHERE  Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW()))''')
        record = self._cr.dictfetchall()
        rec_ids = [item['count'] for item in record]
        hr_applicant_value = rec_ids[0]

        self._cr.execute('''select COUNT(id) from hiring_request WHERE Extract(Year FROM hiring_request.create_date
            ) = Extract(Year FROM DATE(NOW()))''' )
        hiring = self._cr.dictfetchall()
        hiring_request_data_value = [item['count'] for item in hiring]
        hiring_request_value = hiring_request_data_value[0]

        data_year = {
            'leads': hr_applicant_value,
            'hiring': hiring_request_value,
        }
        return data_year

    @api.model
    def crm_month(self):
        """Year CRM Dropdown Filter"""
        # session_user_id = self.env.uid

        self._cr.execute(
            '''select COUNT(id) from hr_applicant WHERE  Extract(MONTH FROM hr_applicant.create_date
        ) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date
        ) = Extract(Year FROM DATE(NOW( )))''')
        record = self._cr.dictfetchall()
        rec_ids = [item['count'] for item in record]
        hr_applicant_value = rec_ids[0]

        self._cr.execute('''select COUNT(id) from hiring_request WHERE Extract(MONTH FROM hiring_request.create_date
        ) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hiring_request.create_date
        ) = Extract(Year FROM DATE(NOW( )))''')
        hiring = self._cr.dictfetchall()
        hiring_request_data_value = [item['count'] for item in hiring]
        hiring_request_value = hiring_request_data_value[0]

        data_month = {
            'leads': hr_applicant_value,
            'hiring': hiring_request_value,
        }
        return data_month
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

    # @api.model
    # def get_sources(self, option):
    #     """Lost Opportunity or Lead Graph"""
    #     month_dict = {}
    #     for i in range(int(option) - 1, -1, -1):
    #         last_month = datetime.now() - relativedelta(months=i)
    #         text = format(last_month, '%B')
    #         month_dict[text] = 0
    #
    #     if option == '1':
    #         day_dict = {}
    #         last_day = date_utils.end_of(fields.Date.today(), "month").strftime("%d")
    #
    #         for i in range(1, int(last_day), 1):
    #             day_dict[i] = 0
    #
    #         self._cr.execute('''select hr_applicant.create_date::date,count(hr_applicant.id), utm_source.name as source from hr_applicant inner join utm_source on utm_source.id = hr_applicant.source_id where hr_applicant.create_date between (now() - interval '1 month') and now()group by hr_applicant.create_date,source order by hr_applicant.create_date;''')
    #         data = self._cr.dictfetchall()
    #
    #         for rec in data:
    #             day_dict[int(rec['create_date'].strftime("%d"))] = rec['count']
    #
    #         test = {'month': list(day_dict.keys()),
    #                 'count': list(day_dict.values())}
    #     else:
    #         month_string = str(int(option)) + ' Months'
    #         self._cr.execute('''select extract(month from hr_applicant.create_date),count(hr_applicant.id),utm_source.name as source
    #             from hr_applicant inner join utm_source on
    #             utm_source.id =hr_applicant.source_id where
    #             hr_applicant.create_date between (now() - interval '%s') and now()
    #             group by extract(month from hr_applicant.create_date),source order by extract(
    #             month from hr_applicant.create_date);''' % month_string)
    #         data = self._cr.dictfetchall()
    #
    #         for rec in data:
    #             datetime_object = datetime.strptime(str(int(rec['date_part'])), "%m")
    #             month_name = datetime_object.strftime("%B")
    #             month_dict[month_name] = rec['count']
    #
    #         test = {'month': list(month_dict.keys()),
    #                 'count': list(month_dict.values())}
    #
    #     return test
