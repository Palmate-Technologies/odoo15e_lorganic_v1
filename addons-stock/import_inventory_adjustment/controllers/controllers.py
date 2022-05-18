# -*- coding: utf-8 -*-
# from odoo import http


# class ImportLotStock(http.Controller):
#     @http.route('/import_lot_stock/import_lot_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_lot_stock/import_lot_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_lot_stock.listing', {
#             'root': '/import_lot_stock/import_lot_stock',
#             'objects': http.request.env['import_lot_stock.import_lot_stock'].search([]),
#         })

#     @http.route('/import_lot_stock/import_lot_stock/objects/<model("import_lot_stock.import_lot_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_lot_stock.object', {
#             'object': obj
#         })
