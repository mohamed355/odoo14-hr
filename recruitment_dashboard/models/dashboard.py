from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz
import calendar
from odoo.tools import date_utils
from datetime import datetime, timedelta


class HrDashboard(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def act_quarter(self):
        """Quarter Activities Dropdown Filter"""
        current_date = datetime.now()
        current_quarter = round((current_date.month - 1) / 3 + 1)
        first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
        last_date = datetime(current_date.year, 3 * current_quarter + 1, 1) \
                    + timedelta(days=-1)
        print(first_date)
        print(last_date)
        act_all = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('res_model', '=', 'hr.applicant')])
        act_over = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('date_deadline', '<', current_date), ('res_model', '=', 'hr.applicant')])
        act_in = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('date_deadline', '>', current_date),
             ('activity_type', '=', 'In Progress')])
        act_not = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Not Completed')])
        act_com = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Completed')])

        act_on = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', first_date), ('date_deadline', '<=', last_date), ('date_deadline', '>', current_date),
             ('activity_type', '=', 'On Hold')])

        data_quarter = {
            'act_all': act_all,
            'act_over': act_over,
            'act_in': act_in,
            'act_not': act_not,
            'act_com': act_com,
            'act_on': act_on,
        }
        return data_quarter

    @api.model
    def act_year(self):
        """Year Activities Dropdown Filter"""
        current_date = datetime.now()
        a = date(date.today().year, 1, 1)
        b = date(date.today().year, 12, 31)
        print(a)
        print(b)
        act_all = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('res_model', '=', 'hr.applicant')])
        act_over = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '<', current_date), ('res_model', '=', 'hr.applicant')])
        act_in = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'In Progress')])
        act_not = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Not Completed')])
        act_com = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Completed')])

        act_on = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'On Hold')])

        data_year = {
            'act_all': act_all,
            'act_over': act_over,
            'act_in': act_in,
            'act_not': act_not,
            'act_com': act_com,
            'act_on': act_on,
        }
        return data_year

    @api.model
    def act_month(self):
        """Year Activities Dropdown Filter"""
        current_date = datetime.now()
        # b = date.today().replace(day=1) - timedelta(days=1)
        # print(last_day_of_prev_month)
        # a = date.today().replace(day=1) + timedelta(days=b.day)
        a = date(current_date.year, current_date.month, 1)
        # b = datetime.date(current_date.year, current_date.month, 1)
        b = date(current_date.year, current_date.month,
                                       calendar.monthrange(current_date.year, current_date.month)[1])

        # print(currentDate)
        # print(lastDayOfM/onth)
        print("a",a)
        print("b",b)
        act_all = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('res_model', '=', 'hr.applicant')])
        act_over = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '<', current_date), ('res_model', '=', 'hr.applicant')])
        act_in = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'In Progress')])
        act_not = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Not Completed')])
        act_com = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'Completed')])

        act_on = self.env['mail.activity'].search_count(
            [('date_deadline', '>=', a), ('date_deadline', '<=', b),
             ('date_deadline', '>', current_date),
             ('activity_type', '=', 'On Hold')])

        data_year = {
            'act_all': act_all,
            'act_over': act_over,
            'act_in': act_in,
            'act_not': act_not,
            'act_com': act_com,
            'act_on': act_on,
        }
        return data_year

    @api.model
    def act_all(self):
        """Quarter Activities Dropdown Filter"""
        current_date = datetime.now()
        current_quarter = round((current_date.month - 1) / 3 + 1)
        first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
        last_date = datetime(current_date.year, 3 * current_quarter + 1, 1) \
                    + timedelta(days=-1)
        print(first_date)
        print(last_date)
        act_all = self.env['mail.activity'].search_count(
            [('res_model', '=', 'hr.applicant')])
        act_over = self.env['mail.activity'].search_count(
            [('date_deadline', '<', current_date),('res_model', '=', 'hr.applicant')])
        act_in = self.env['mail.activity'].search_count(
            [('date_deadline', '>', current_date),
             ('activity_type', '=', 'In Progress'),('res_model', '=', 'hr.applicant')])
        act_not = self.env['mail.activity'].search_count(
            [('date_deadline', '>', current_date),
             ('activity_type', '=', 'Not Completed'),('res_model', '=', 'hr.applicant')])
        act_com = self.env['mail.activity'].search_count(
            [('date_deadline', '>', current_date),
             ('activity_type', '=', 'Completed'),('res_model', '=', 'hr.applicant')])

        act_on = self.env['mail.activity'].search_count(
            [('create_date', '>', current_date),
             ('activity_type', '=', 'On Hold'),('res_model', '=', 'hr.applicant')])

        data_all = {
            'act_all': act_all,
            'act_over': act_over,
            'act_in': act_in,
            'act_not': act_not,
            'act_com': act_com,
            'act_on': act_on,
        }
        return data_all

    @api.model
    def get_data(self):
        hr_applicant = self.env['hr.applicant'].search([])
        open_hiring = self.env['hiring.request'].search([])
        com_hiring = self.env['hiring.request'].search_count([("stage_id.name", '=', "Completed")])
        com_app = self.env['hr.applicant'].search_count([("stage_id.name", '=', "Offer Accepted")])
        rej_app = self.env['hr.applicant'].search_count([("stage_id.name", '=', "Offer Rejected")])
        ac_app = self.env['hr.applicant'].search_count([("stage_id.name", '=', "Offer Accepted")])
        h_a = 0
        duration_list = []
        for app in hr_applicant:
            if app.hiring_ids:
                print("App", app.acc_date)
                print("hiring", app.hiring_ids[0].acc_date)
                if app.acc_date and app.hiring_ids[0].acc_date:
                    duration = abs(app.acc_date - app.hiring_ids[0].acc_date)
                    duration_list.append(duration.days)
        print("Duration", duration_list)
        print("Duration", sum(duration_list))

        if round(len(hr_applicant) / len(open_hiring)):
            h_a = round(len(hr_applicant) / len(open_hiring))
        try:
            app_3 = round((com_app / (rej_app + ac_app)) * 100)
        except ZeroDivisionError:
            app_3 = 0

        try:
            app_4 = round((sum(duration_list) / len(hr_applicant)) * 100)
        except ZeroDivisionError:
            app_4 = 0

        h_com = 0
        if round(len(hr_applicant) / len(open_hiring)):
            h_com = round((len(open_hiring) / com_hiring / 100) * 100)
        return {
            'open_hiring': len(open_hiring),
            'hr_applicant': len(hr_applicant),
            'h_a': h_a,
            'h_com': h_com,
            'app_3': app_3,
            'app_4': app_4,

        }

    @api.model
    def crm_quarter(self):
        """Quarter CRM Dropdown Filter"""
        current_date = datetime.now()
        current_quarter = round((current_date.month - 1) / 3 + 1)
        first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
        last_date = datetime(current_date.year, 3 * current_quarter + 1, 1) \
                    + timedelta(days=-1)
        print(first_date)
        print(last_date)
        hr_applicant = self.env['hr.applicant'].search(
            [('create_date', '>=', first_date), ('create_date', '<=', last_date)])
        open_hiring = self.env['hiring.request'].search(
            [('create_date', '>=', first_date), ('create_date', '<=', last_date)])
        com_hiring = self.env['hiring.request'].search_count(
            [("stage_id.name", '=', "Completed"), ('create_date', '>=', first_date), ('create_date', '<=', last_date)])
        com_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', first_date),
             ('create_date', '<=', last_date)])
        rej_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Rejected"), ('create_date', '>=', first_date),
             ('create_date', '<=', last_date)])
        ac_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', first_date),
             ('create_date', '<=', last_date)])
        h_a = 0
        duration_list = []
        for app in hr_applicant:
            if app.hiring_ids:
                print("App", app.acc_date)
                print("hiring", app.hiring_ids[0].acc_date)
                if app.acc_date and app.hiring_ids[0].acc_date:
                    duration = abs(app.acc_date - app.hiring_ids[0].acc_date)
                    duration_list.append(duration.days)
        print("Duration", duration_list)
        print("Duration", sum(duration_list))

        if round(len(hr_applicant) / len(open_hiring)):
            h_a = round(len(hr_applicant) / len(open_hiring))
        try:
            app_3 = round((com_app / (rej_app + ac_app)) * 100)
        except ZeroDivisionError:
            app_3 = 0

        try:
            app_4 = round((sum(duration_list) / len(hr_applicant)) * 100)
        except ZeroDivisionError:
            app_3 = 0

        h_com = 0
        if round(len(hr_applicant) / len(open_hiring)):
            h_com = round((len(open_hiring) / com_hiring / 100) * 100)
        # session_user_id = self.env.uid

        self._cr.execute('''select COUNT(id) from hiring_request Where Extract(QUARTER FROM hiring_request.create_date) = Extract(QUARTER FROM DATE(NOW()))
            AND Extract(Year FROM hiring_request.create_date) = Extract(Year FROM DATE(NOW()))
            ''')
        record = self._cr.dictfetchall()
        rec_ids = [item['count'] for item in record]
        hiring_request_value = rec_ids[0]

        self._cr.execute('''select COUNT(id) from hr_applicant  Where  Extract(QUARTER FROM hr_applicant.create_date
            ) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date
            ) = Extract(Year FROM DATE(NOW( )))''')
        hr_applicant_data = self._cr.dictfetchall()
        hr_applicant_data_value = [item['count'] for item in hr_applicant_data]
        hr_applicant_value = hr_applicant_data_value[0]

        data_quarter = {
            'leads': hr_applicant_value,
            'hiring': hiring_request_value,
            'h_a': h_a,
            'h_com': h_com,
            'app_3': app_3,
            'app_4': app_4,
        }
        return data_quarter

    @api.model
    def crm_year(self):

        a = date(date.today().year, 1, 1)
        b = date(date.today().year, 12, 31)
        """Year CRM Dropdown Filter"""
        hr_applicant = self.env['hr.applicant'].search([('create_date', '>=', a), ('create_date', '<=', b)])
        open_hiring = self.env['hiring.request'].search([('create_date', '>=', a), ('create_date', '<=', b)])
        com_hiring = self.env['hiring.request'].search_count(
            [("stage_id.name", '=', "Completed"), ('create_date', '>=', a), ('create_date', '<=', b)])
        com_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', a), ('create_date', '<=', b)])
        rej_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Rejected"), ('create_date', '>=', a), ('create_date', '<=', b)])
        ac_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', a), ('create_date', '<=', b)])
        h_a = 0
        duration_list = []
        for app in hr_applicant:
            if app.hiring_ids:
                print("App", app.acc_date)
                print("hiring", app.hiring_ids[0].acc_date)
                if app.acc_date and app.hiring_ids[0].acc_date:
                    duration = abs(app.acc_date - app.hiring_ids[0].acc_date)
                    duration_list.append(duration.days)
        print("Duration", duration_list)
        print("Duration", sum(duration_list))

        if round(len(hr_applicant) / len(open_hiring)):
            h_a = round(len(hr_applicant) / len(open_hiring))
        try:
            app_3 = round((com_app / (rej_app + ac_app)) * 100)
        except ZeroDivisionError:
            app_3 = 0

        try:
            app_4 = round((sum(duration_list) / len(hr_applicant)) * 100)
        except ZeroDivisionError:
            app_3 = 0

        h_com = 0
        if round(len(hr_applicant) / len(open_hiring)):
            h_com = round((len(open_hiring) / com_hiring / 100) * 100)
        self._cr.execute(
            '''select COUNT(id) from hr_applicant WHERE  Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW()))''')
        record = self._cr.dictfetchall()
        rec_ids = [item['count'] for item in record]
        hr_applicant_value = rec_ids[0]

        self._cr.execute('''select COUNT(id) from hiring_request WHERE Extract(Year FROM hiring_request.create_date
            ) = Extract(Year FROM DATE(NOW()))''')
        hiring = self._cr.dictfetchall()
        hiring_request_data_value = [item['count'] for item in hiring]
        hiring_request_value = hiring_request_data_value[0]

        data_year = {
            'leads': hr_applicant_value,
            'hiring': hiring_request_value,
            'h_a': h_a,
            'h_com': h_com,
            'app_3': app_3,
            'app_4': app_4,
            # 'stages_list': stages_list,
        }
        return data_year

    @api.model
    def crm_month(self):
        """Year CRM Dropdown Filter"""
        # session_user_id = self.env.uid
        last_day_of_prev_month = date(datetime.now().year, datetime.now().month,
                                       calendar.monthrange(datetime.now().year, datetime.now().month)[1])

        print(last_day_of_prev_month)
        start_day_of_prev_month = date(datetime.now().year, datetime.now().month, 1)
        hr_applicant = self.env['hr.applicant'].search(
            [('create_date', '>=', start_day_of_prev_month), ('create_date', '<=', last_day_of_prev_month)])
        open_hiring = self.env['hiring.request'].search(
            [('create_date', '>=', start_day_of_prev_month), ('create_date', '<=', last_day_of_prev_month)])
        com_hiring = self.env['hiring.request'].search_count(
            [("stage_id.name", '=', "Completed"), ('create_date', '>=', start_day_of_prev_month),
             ('create_date', '<=', last_day_of_prev_month)])
        com_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', start_day_of_prev_month),
             ('create_date', '<=', last_day_of_prev_month)])
        rej_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Rejected"), ('create_date', '>=', start_day_of_prev_month),
             ('create_date', '<=', last_day_of_prev_month)])
        ac_app = self.env['hr.applicant'].search_count(
            [("stage_id.name", '=', "Offer Accepted"), ('create_date', '>=', start_day_of_prev_month),
             ('create_date', '<=', last_day_of_prev_month)])
        h_a = 0
        duration_list = []
        for app in hr_applicant:
            if app.hiring_ids:
                print("App", app.acc_date)
                print("hiring", app.hiring_ids[0].acc_date)
                if app.acc_date and app.hiring_ids[0].acc_date:
                    duration = abs(app.acc_date - app.hiring_ids[0].acc_date)
                    duration_list.append(duration.days)
        print("Duration", duration_list)
        print("Duration", sum(duration_list))

        try:
            h_a = round(len(hr_applicant) / len(open_hiring))
        except ZeroDivisionError:
            h_a = 0
        app_3 = 0
        try:
            app_3 = round((com_app / (rej_app + ac_app)) * 100)
        except ZeroDivisionError:
            app_3 = 0
        app_4 = 0
        try:
            app_4 = round((sum(duration_list) / len(hr_applicant)) * 100)
        except ZeroDivisionError:
            app_4 = 0

        h_com = 0
        try:
            h_com = round((len(open_hiring) / com_hiring / 100) * 100)
        except ZeroDivisionError:
            h_com = 0
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
            'h_a': h_a,
            'h_com': h_com,
            'app_3': app_3,
            'app_4': app_4,
        }
        return data_month

    @api.model
    def get_stages(self):
        """Recent Activities Table"""
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
    def get_recruiter_year(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,res_partner.name as partner from 
        hr_applicant  inner join res_partner on 
        res_partner.id =hr_applicant.partner_id  WHERE Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by partner ORDER BY co DESC'''

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
        final = [total_app, partner_name]
        return final

    @api.model
    def get_recruiter_month(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,res_partner.name as partner from 
            hr_applicant  inner join res_partner on 
            res_partner.id =hr_applicant.partner_id  WHERE  Extract(MONTH FROM hr_applicant.create_date) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW( ))) group by partner ORDER BY co DESC'''

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
        final = [total_app, partner_name]
        return final

    @api.model
    def get_recruiter_quarter(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,res_partner.name as partner from 
                hr_applicant  inner join res_partner on 
                res_partner.id =hr_applicant.partner_id  Where Extract(QUARTER FROM hr_applicant.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by partner ORDER BY co DESC'''

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
        final = [total_app, partner_name]
        return final

    @api.model
    def get_recruiter_all(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,res_partner.name as partner from 
                    hr_applicant  inner join res_partner on 
                    res_partner.id = hr_applicant.partner_id group by partner ORDER BY co DESC'''

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
        final = [total_app, partner_name]
        return final

    @api.model
    def get_jobs_year(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hr_job.name as job from 
            hr_applicant inner join hr_job on 
            hr_job.id =hr_applicant.job_id WHERE Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by job  ORDER BY co DESC'''

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
    def get_jobs_all(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hr_job.name as job from 
                hr_applicant inner join hr_job on 
                hr_job.id =hr_applicant.job_id group by job  ORDER BY co DESC'''

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
    def get_jobs_quarter(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hr_job.name as job from 
                hr_applicant inner join hr_job on 
                hr_job.id =hr_applicant.job_id Where Extract(QUARTER FROM hr_applicant.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by job  ORDER BY co DESC'''

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
    def get_jobs_month(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hr_job.name as job from 
                    hr_applicant inner join hr_job on 
                    hr_job.id =hr_applicant.job_id WHERE  Extract(MONTH FROM hr_applicant.create_date) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW( ))) group by job  ORDER BY co DESC'''

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
    def get_act_don_year(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hiring_stage.name as type from 
                hiring_request inner join hiring_stage on hiring_stage.id = hiring_request.stage_id WHERE Extract(Year FROM hiring_stage.create_date) = Extract(Year FROM DATE(NOW())) group by hiring_stage.name ORDER BY co DESC'''

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
    def get_act_don_quarter(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hiring_stage.name as type from 
                hiring_request inner join hiring_stage on hiring_stage.id = hiring_request.stage_id Where Extract(QUARTER FROM hiring_request.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM hiring_request.create_date) = Extract(Year FROM DATE(NOW())) group by hiring_stage.name ORDER BY co DESC'''

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
    def get_act_don_all(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hiring_stage.name as type from 
                    hiring_request inner join hiring_stage on hiring_stage.id = hiring_request.stage_id  group by hiring_stage.name ORDER BY co DESC'''

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
    def get_act_don_month(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,hiring_stage.name as type from 
                hiring_request inner join hiring_stage on hiring_stage.id = hiring_request.stage_id WHERE  Extract(MONTH FROM hiring_request.create_date) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hiring_request.create_date) = Extract(Year FROM DATE(NOW( ))) group by hiring_stage.name ORDER BY co DESC'''

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
    def get_sources_year(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,utm_source.name as source from
                hr_applicant inner join utm_source on
                utm_source.id =hr_applicant.source_id WHERE Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by source ORDER BY co DESC'''

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

    @api.model
    def get_sources_month(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,utm_source.name as source from
                    hr_applicant inner join utm_source on
                    utm_source.id =hr_applicant.source_id WHERE  Extract(MONTH FROM hr_applicant.create_date) = Extract(MONTH FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW( ))) group by source ORDER BY co DESC'''

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

    @api.model
    def get_sources_quarter(self):
        company_id = self.env.company.id

        query = '''select count(*) as co,utm_source.name as source from
                        hr_applicant inner join utm_source on
                        utm_source.id =hr_applicant.source_id Where Extract(QUARTER FROM hr_applicant.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM hr_applicant.create_date) = Extract(Year FROM DATE(NOW())) group by source ORDER BY co DESC'''

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

    @api.model
    def get_sources_all(self):
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

    @api.model
    def get_stages_this_year(self):

        month_list = []
        for i in range(11, -1, -1):
            l_month = datetime.now() - relativedelta(months=i)
            text = format(l_month, '%B')
            month_list.append(text)

        states_arg = ""

        self._cr.execute(('''select count(*) as income ,stage_id as stage from hr_applicant where 
                                to_char(DATE(NOW()), 'YY') = to_char(hr_applicant.create_date, 'YY')
                                %s  group by month ''') % (states_arg))
        record = self._cr.dictfetchall()

        records = []
        for month in month_list:
            last_month_inc = list(filter(lambda m: m['month'].strip() == month, record))

            if not last_month_inc:
                records.append({
                    'month': month,
                    'profit': 0.0,
                })

            else:

                last_month_inc[0].update({
                    'profit': last_month_inc[0]['income']
                })
                records.append(last_month_inc[0])

        month = []
        profit = []
        for rec in records:
            month.append(rec['month'])
            profit.append(rec['profit'])
        return {
            'profit': profit,
            'month': month
        }
