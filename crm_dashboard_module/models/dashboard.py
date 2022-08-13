from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar


class Dashboard(models.Model):
    _inherit = 'crm.lead'
    for_date = fields.Date(string="Forecasting Date", required=False, )

    @api.model
    def get_data(self):
        today = datetime.today()
        datem_1 = datetime(today.year, today.month, 1)
        last_day= calendar.monthrange(today.year, today.month)[1]
        datem_2 = datetime(today.year, today.month, last_day)
        print("Date",datem_1)
        print("Date Calendar",calendar.monthrange(today.year, today.month)[1])
        # domain = [('date_order','>=',default_data)]
        crm_lead=self.env['crm.lead'].search([])
        crm_activity=self.env['mail.activity'].search([('res_model_id.model','=','crm.lead'),('activity_type_id.category','=','meeting')])
        crm_activity_meeting=self.env['mail.activity'].search([('res_model_id.model','=','crm.lead'),('activity_type_id.category','=','meeting')])
        crm_activity_call=self.env['mail.activity'].search([('res_model_id.model','=','crm.lead'),('activity_type_id.category','=','phonecall')])
        open_opp=self.env['crm.lead'].search([('probability', '!=', 100), ('type', '=', 'opportunity')])
        close_to=self.env['crm.lead'].search([('date_deadline', '>=', datem_1),('date_deadline', '<=', datem_2)])
        crm_opp=self.env['crm.lead'].search([('type','=','opportunity')])
        return {
            'total_lead':len(crm_lead),
            'total_opp':len(crm_opp),
            'total_activity':len(crm_activity),
            'crm_activity_call':len(crm_activity_call),
            'open_opp':len(open_opp),
            'close_to':len(close_to),
        }

    @api.model
    def get_the_annual_target(self):
        """Annual Target: Year To Date Graph"""
        session_user_id = self.env.uid

        self._cr.execute('''SELECT res_users.id,res_users.sales,res_users.sale_team_id,
            (SELECT crm_team.invoiced_target FROM crm_team WHERE crm_team.id = res_users.sale_team_id)
            FROM res_users WHERE res_users.sales is not null and res_users.id=%s
            AND res_users.sale_team_id is not null;''' % session_user_id)
        data2 = self._cr.dictfetchall()

        sales = []
        inv_target = []
        team_id = 0
        for rec in data2:
            sales.append(rec['sales'])
            inv_target.append(rec['invoiced_target'])
            team_id = rec['sale_team_id']
        target_annual = (sum(sales) + sum(inv_target))

        if self.env.user.has_group('sales_team.group_sale_manager'):
            self._cr.execute('''SELECT res_users.id,res_users.sales,res_users.sale_team_id,
                (SELECT crm_team.invoiced_target FROM crm_team WHERE
                crm_team.id = res_users.sale_team_id) FROM res_users WHERE res_users.id = %s
                AND res_users.sales is not null;''' % session_user_id)
            data3 = self._cr.dictfetchall()

            sales = []
            inv_target = []
            for rec in data3:
                sales.append(rec['sales'])
                inv_target.append(rec['invoiced_target'])
            ytd_target = (sum(sales) + sum(inv_target))

            self._cr.execute('''select sum(expected_revenue) from crm_lead where stage_id=4
                and team_id=%s AND Extract(Year FROM date_closed)=Extract(Year FROM DATE(NOW(
                )))''' % team_id)
            achieved_won_data = self._cr.dictfetchall()
            achieved_won = [item['sum'] for item in achieved_won_data]

        else:
            self._cr.execute('''SELECT res_users.id,res_users.sales FROM res_users
                WHERE res_users.id = %s AND res_users.sales is not null;''' % session_user_id)
            data4 = self._cr.dictfetchall()

            sales = []
            for rec in data4:
                sales.append(rec['sales'])
            ytd_target = (sum(sales))

            self._cr.execute('''select sum(expected_revenue) from crm_lead where stage_id=4
                and user_id=%s AND Extract(Year FROM date_closed)=Extract(Year FROM DATE(NOW(
                )))''' % session_user_id)
            achieved_won_data = self._cr.dictfetchall()
            achieved_won = [item['sum'] for item in achieved_won_data]

        won = achieved_won[0]
        if won is None:
            won = 0
        value = [target_annual, ytd_target, won]
        name = ["Annual Target", "YtD target", "Won"]
        final = [value, name]

        return final

    @api.model
    def get_recent_activities(self):
        """Recent Activities Table"""
        today = fields.date.today()
        recent_week = today - relativedelta(days=7)
        self._cr.execute('''select mail_activity.activity_type_id,mail_activity.date_deadline,
        mail_activity.summary,mail_activity.res_name,(SELECT mail_activity_type.name
        FROM mail_activity_type WHERE mail_activity_type.id = mail_activity.activity_type_id ),
        mail_activity.user_id FROM mail_activity WHERE res_model = 'crm.lead'  GROUP BY mail_activity.activity_type_id,
        mail_activity.date_deadline,mail_activity.summary,mail_activity.res_name,mail_activity.user_id
        order by mail_activity.date_deadline desc''')
        data = self._cr.fetchall()
        activities = []
        for record in data:
            if record[4] == 'Meeting':
                print(record)
                user_id = record[5]
                user_id_obj = self.env['res.users'].browse(user_id)
                record_list = list(record)
                record_list[5] = user_id_obj.name
                activities.append(record_list)
        print("activities",activities)
        return {'activities': activities}

    @api.model
    def get_recent_todo_activities(self):
        """Recent Activities Table To Do"""
        today = fields.date.today()
        recent_week = today - relativedelta(days=7)
        self._cr.execute('''select mail_activity.activity_type_id,mail_activity.date_deadline,
            mail_activity.summary,mail_activity.res_name,(SELECT mail_activity_type.name
            FROM mail_activity_type WHERE mail_activity_type.id = mail_activity.activity_type_id ),
            mail_activity.user_id FROM mail_activity WHERE res_model = 'crm.lead'  GROUP BY mail_activity.activity_type_id,
            mail_activity.date_deadline,mail_activity.summary,mail_activity.res_name,mail_activity.user_id
            order by mail_activity.date_deadline desc''')
        data = self._cr.fetchall()
        activities = []
        for record in data:
            if record[4] == 'To Do':
                print(record)
                user_id = record[5]
                user_id_obj = self.env['res.users'].browse(user_id)
                record_list = list(record)
                record_list[5] = user_id_obj.name
                activities.append(record_list)
        print("activities", activities)
        return {'activities': activities}
    # def get_recent_todo_activities(self):
    #     """Recent Activities Table"""
    #     today = fields.date.today()
    #     recent_week = today - relativedelta(days=7)
    #     self._cr.execute('''select mail_activity.activity_type_id,mail_activity.date_deadline,
    #     mail_activity.summary,mail_activity.res_name,(SELECT mail_activity_type.name
    #     FROM mail_activity_type WHERE mail_activity_type.id = mail_activity.activity_type_id ),
    #     mail_activity.user_id FROM mail_activity WHERE res_model = 'crm.lead'  GROUP BY mail_activity.activity_type_id,
    #     mail_activity.date_deadline,mail_activity.summary,mail_activity.res_name,mail_activity.user_id
    #     order by mail_activity.date_deadline desc''')
    #     data = self._cr.fetchall()
    #     activities = []
    #     for record in data:
    #
    #             print(record)
    #             user_id = record[5]
    #             user_id_obj = self.env['res.users'].browse(user_id)
    #             record_list = list(record)
    #             record_list[5] = user_id_obj.name
    #             activities.append(record_list)
    #     print("activities todo",activities)
    #     return {'activities': activities}

    @api.model
    def get_recent_call_activities(self):
        """Recent Activities Table"""
        today = fields.date.today()
        recent_week = today - relativedelta(days=7)
        self._cr.execute('''select mail_activity.activity_type_id,mail_activity.date_deadline,
            mail_activity.summary,mail_activity.res_name,(SELECT mail_activity_type.name
            FROM mail_activity_type WHERE mail_activity_type.id = mail_activity.activity_type_id ),
            mail_activity.user_id FROM mail_activity WHERE res_model = 'crm.lead'  GROUP BY mail_activity.activity_type_id,
            mail_activity.date_deadline,mail_activity.summary,mail_activity.res_name,mail_activity.user_id
            order by mail_activity.date_deadline desc''')
        data = self._cr.fetchall()
        activities = []
        for record in data:
            if record[4] == 'Call':
                print(record)
                user_id = record[5]
                user_id_obj = self.env['res.users'].browse(user_id)
                record_list = list(record)
                record_list[5] = user_id_obj.name
                activities.append(record_list)
        print("activities", activities)
        return {'activities': activities}
    @api.model
    def get_the_sales_activity(self):
        """Sales Activity Pie"""
        self._cr.execute('''select mail_activity_type.name,COUNT(*) from mail_activity
            inner join mail_activity_type on mail_activity.activity_type_id = mail_activity_type.id
            where mail_activity.res_model = 'crm.lead' GROUP BY mail_activity_type.name''')
        data = self._cr.dictfetchall()

        name = []
        for record in data:
            name.append(record.get('name'))

        count = []
        for record in data:
            count.append(record.get('count'))

        final = [count, name]
        return final

    @api.model
    def get_lead_stage_data(self):
        """funnel chart"""
        stage_ids = self.env["crm.stage"].search([])
        crm_list = []
        for stage in stage_ids:
            leads = self.search_count([("stage_id", "=", stage.id),('type','=','opportunity')])
            crm_list.append((stage.name, int(leads)))
        return crm_list

    @api.model
    def crm_lead_graph(self):
        # """Leads Group By Source Pie"""
        """Lost Leads by Stage Pie"""
        self._cr.execute('''select stage_id, sum(expected_revenue),(SELECT name FROM crm_stage
                WHERE id = stage_id) from crm_lead  group by stage_id''')
        data1 = self._cr.dictfetchall()


        name = []
        for rec in data1:
            name.append(rec.get('name'))

        sum = []
        for rec in data1:
            sum.append(rec.get('sum'))

        lost_leads_stage = [sum, name]
        return lost_leads_stage
