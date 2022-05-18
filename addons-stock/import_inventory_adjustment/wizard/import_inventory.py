import xlrd
import base64
from odoo.exceptions import UserError
from odoo import fields, models, api
from datetime import timedelta
import datetime


class ImportInventory(models.TransientModel):
    _name = 'import.inventory'
    _description = 'Import Inventory'

    excel_file = fields.Binary(string="Excel File")
    location_id = fields.Many2one('stock.location', string="Location", domain=[('usage','=','internal')])

    def action_import(self):
        self.ensure_one()
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = book.sheet_by_index(0)

        data = []
        Product = self.env['product.product']
        Lot = self.env['stock.production.lot']
        for row in range(1, sheet.nrows):
            default_code = str(int(sheet.cell(row, 0).value))
            products = Product.search([('default_code', '=', default_code)])
            if not products:
                raise UserError(('No Product found with code:', default_code))

            lot_id = False
            lot_name = str(int(sheet.cell(row, 2).value)),
            if lot_name:
                lots = Lot.search([('name', '=', lot_name),('product_id','=',products[0].id)])
                if not lots:
                    raise UserError(('No Lot found: '+str(lot_name)+'. '+'for product '+str(default_code)))
                lot_id = lots[0].id

            line = {
                'qty': float(sheet.cell(row, 1).value),
                'product_id':products[0].id,
                'lot_id':lot_id,
            }
            # print("Line: ",line)
            data.append(line)
        print("Data: ",data)
        self.create_adjustments(data)

    def create_adjustments(self, data):
        Quant = self.env['stock.quant']
        location_id = self.location_id.id
        for row in data:
            quant = Quant.create({
                'location_id':location_id,
                'product_id':row.get('product_id'),
                'lot_id':row.get('lot_id',False),
                'inventory_quantity':row.get('qty', 0),
                })
            print("quant created: ",quant)

        return True

