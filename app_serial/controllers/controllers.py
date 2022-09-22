# -*- coding: utf-8 -*-
# from odoo import http


# class AppSerial(http.Controller):
#     @http.route('/app_serial/app_serial', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/app_serial/app_serial/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('app_serial.listing', {
#             'root': '/app_serial/app_serial',
#             'objects': http.request.env['app_serial.app_serial'].search([]),
#         })

    # @http.route('/app_serial/app_serial/objects/<model("hr.applicant"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('hr_applicant.object', {
    #         'object': obj
    #     })
