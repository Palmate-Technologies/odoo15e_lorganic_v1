# -*- coding: utf-8 -*-
# from odoo import http


# class ImportPosOrdersChanges(http.Controller):
#     @http.route('/import_pos_orders_changes/import_pos_orders_changes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_pos_orders_changes/import_pos_orders_changes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_pos_orders_changes.listing', {
#             'root': '/import_pos_orders_changes/import_pos_orders_changes',
#             'objects': http.request.env['import_pos_orders_changes.import_pos_orders_changes'].search([]),
#         })

#     @http.route('/import_pos_orders_changes/import_pos_orders_changes/objects/<model("import_pos_orders_changes.import_pos_orders_changes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_pos_orders_changes.object', {
#             'object': obj
#         })
