from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager

class CustomerPortal(portal.CustomerPortal):
    @http.route(['/portal/attendance/check_in_check_out'], type='http', auth="user", website=True)
    def portal_attendance(self, **kw):
        return request.render('gs_portal_attendances.portal_attendace', {})

    @http.route(['/portal/attendance/employee'], type='json', auth="user", website=True)
    def portal_employee_info_attendance(self, **kw):
        rec = request.env['hr.employee.public'].sudo().search([('user_id', '=', request.env.user.id), ('company_id', '=', request.env.user.company_id.id)])
        if rec:
            return {
                'employee_id': rec.employee_id.id if rec.employee_id else False,
                'employee_name': rec.employee_id.name if rec.employee_id else '',
                'employee_state': rec.attendance_state,
                'employee_hours_today': rec.hours_today
           }
        else:
           return {
                'employee_id': '',
                'employee_name': '',
                'employee_state': '',
                'employee_hours_today':''
           }

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user = request.env.user
        HrAttendance = request.env['hr.attendance']
        if 'attendances_count' in counters:
            if not user.employee_id:
                values['attendances_count'] = 0
            else:
                values['attendances_count'] = HrAttendance.sudo().search_count(self._prepare_attendace_domain(user))
        return values

    def _prepare_attendace_domain(self, user):
        return [
            ('employee_id', '=', user.employee_id.id)
        ]

    def _get_attendance_searchbar_sortings(self):
        return {
            'check_in': {'label': _('Check In'), 'order': 'check_in desc'},
            'check_out': {'label': _('Check Out'), 'order': 'check_in desc'},
            'worked_hours': {'label': _('Work Hourse'), 'order': 'worked_hours desc'},
        }

    @http.route(['/my/attendances', '/my/attendances/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_attendances(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        HrAttendance = request.env['hr.attendance']
        domain = self._prepare_attendace_domain(user)
        searchbar_sortings = self._get_attendance_searchbar_sortings()

        # default sortby order
        if not sortby:
            sortby = 'check_in'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        attendances_count = HrAttendance.sudo().search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/attendances",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=attendances_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        attendances = HrAttendance.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_attendances_history'] = attendances.ids[:100]

        values.update({
            'date': date_begin,
            'attendances': attendances.sudo(),
            'page_name': 'attendance',
            'pager': pager,
            'default_url': '/my/attendances',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("gs_portal_attendances.portal_my_attendances", values)