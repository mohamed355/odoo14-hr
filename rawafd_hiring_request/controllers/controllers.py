# -*- coding: utf-8 -*-
from odoo import http

# class RawafdHiringRequest(http.Controller):
#     @http.route('/rawafd_hiring_request/rawafd_hiring_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rawafd_hiring_request/rawafd_hiring_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rawafd_hiring_request.listing', {
#             'root': '/rawafd_hiring_request/rawafd_hiring_request',
#             'objects': http.request.env['rawafd_hiring_request.rawafd_hiring_request'].search([]),
#         })

#     @http.route('/rawafd_hiring_request/rawafd_hiring_request/objects/<model("rawafd_hiring_request.rawafd_hiring_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rawafd_hiring_request.object', {
#             'object': obj
#         })