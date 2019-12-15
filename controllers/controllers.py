# -*- coding: utf-8 -*-
from openerp import http

# class Audit(http.Controller):
#     @http.route('/audit/audit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/audit/audit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('audit.listing', {
#             'root': '/audit/audit',
#             'objects': http.request.env['audit.audit'].search([]),
#         })

#     @http.route('/audit/audit/objects/<model("audit.audit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('audit.object', {
#             'object': obj
#         })