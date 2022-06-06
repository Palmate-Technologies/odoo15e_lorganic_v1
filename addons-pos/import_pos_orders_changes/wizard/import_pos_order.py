import xlrd
import base64
from odoo.exceptions import UserError
from odoo import fields, models, api
from datetime import timedelta
import datetime


class ImportPosOrder(models.TransientModel):
    _name = 'import.pos.order'
    _description = 'Import POS Order'

    excel_file = fields.Binary(string="Excel File")
    session_id = fields.Many2one('pos.session', string="Session", required=True, domain=[('state','=','opened')])

    def _get_order_line(self, sheet, row):
        order_line = {
            'barcode': sheet.cell(rowx=row, colx=10).value,
            'unit': sheet.cell(rowx=row, colx=11).value,

            'qty': sheet.cell(rowx=row, colx=12).value,
            'unit_price': sheet.cell(rowx=row, colx=13).value,
            'disc_perc': sheet.cell(rowx=row, colx=14).value,
            'tax_name': sheet.cell(rowx=row, colx=15).value,
            'subtotal_wo_tax': sheet.cell(rowx=row, colx=16).value,
            'subtotal': sheet.cell(rowx=row, colx=17).value,
        }
        return order_line

    def _get_payment_line(self, sheet, book, row):
        payment_date = sheet.cell_value(rowx=row, colx=23)
        payment_date = datetime.datetime(*xlrd.xldate_as_tuple(payment_date, book.datemode))
        payment_line = {
            'payment_method': sheet.cell(rowx=row, colx=20).value,
            'amount': sheet.cell(rowx=row, colx=21).value,
            'payment_name': sheet.cell(rowx=row, colx=22).value,
            'payment_date': payment_date,
        }
        return payment_line

    def action_import_pos_order(self):
        self.ensure_one()
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = book.sheet_by_index(0)
        session_id = self.session_id.id

        data = []
        order = {}
        for row in range(1, sheet.nrows):
            order_number = sheet.cell(rowx=row, colx=0).value
            if order_number:
                # if row >=2:
                if len(order):
                    data.append(order)
                if order_number == 'End':
                    break;
                date_order = sheet.cell_value(rowx=row, colx=2)
                date_order = datetime.datetime(*xlrd.xldate_as_tuple(date_order, book.datemode))

                order = {
                    'order_number':order_number,
                    'date_order':date_order,
                    'pos_reference':sheet.cell(rowx=row, colx=3).value,
                    'customer':sheet.cell(rowx=row, colx=4).value,
                    'customer_phone':sheet.cell(rowx=row, colx=5).value,
                    'user':sheet.cell(rowx=row, colx=6).value,
                    'total':sheet.cell(rowx=row, colx=7).value,
                    'status':sheet.cell(rowx=row, colx=8).value,
                    'fiscal_position':sheet.cell(rowx=row, colx=9).value,
                    'taxes':sheet.cell(rowx=row, colx=18).value,
                    'paid':sheet.cell(rowx=row, colx=19).value,
                    'pricelist':sheet.cell(rowx=row, colx=24).value,
                    'loyalty_points':sheet.cell(rowx=row, colx=25).value,
                    'session_id':session_id,

                }
                order_lines = []
                order_lines.append(self._get_order_line(sheet, row))
                order['order_lines'] = order_lines

                # payment lines
                payment_lines = []
                payment_method = sheet.cell(rowx=row, colx=20).value
                if payment_method:
                    payment_lines.append(self._get_payment_line(sheet, book, row))
                order['payment_lines'] = payment_lines

            else:
                order_lines.append(self._get_order_line(sheet, row))
                order['order_lines'] = order_lines

                # payment lines
                payment_method = sheet.cell(rowx=row, colx=20).value
                if payment_method:
                    payment_lines.append(self._get_payment_line(sheet, book, row))
                    order['payment_lines'] = payment_lines

        self.create_pos_orders(data)

    def create_pos_orders(self, data):
        user_data = partner_data = fiscal_data = pricelist_data = product_data = tax_data = payment_data = {}

        User = self.env['res.users']
        Partner = self.env['res.partner']
        Fiscal = self.env['account.fiscal.position']
        PriceList = self.env['product.pricelist']
        Product = self.env['product.product']
        Tax = self.env['account.tax']
        Pos = self.env['pos.order']
        PaymentMethod = self.env['pos.payment.method']
        config = self.session_id.config_id

        for order in data:
            user = order.get('user', False)
            user_id = user_data.get(user, False)
            if not user_id:
                user_ids = User.search([('name','=',user)])
                if user_ids:
                    user_id = user_ids[0].id
                    user_data[user] = user_id

            partner_id = False
            customer_phone = order.get('customer_phone', False)
            if customer_phone:
                partner_id = partner_data.get(customer_phone, False)
                if not partner_id:
                    partner_ids = Partner.search([('phone','=',customer_phone)])
                    if partner_ids:
                        partner_id = partner_ids[0].id
                        partner_data[customer_phone] = partner_id
            if not partner_id and order.get('customer', False):
                customer_name = order.get('customer', False)
                partner_ids = Partner.search([('name', '=', customer_name)])
                if partner_ids:
                    partner_id = partner_ids[0].id
                    partner_data[customer_name] = partner_id
            if not partner_id and order.get('customer', False):
                partner = Partner.create({
                    'name':order.get('customer',''),
                    'phone':order.get('customer_phone',''),
                    'customer_rank':1,
                })
                partner_id =partner.id

            fiscal_position_id = False
            fiscal_position = order.get('fiscal_position', False)
            if fiscal_position:
                fiscal_position_id = fiscal_data.get(fiscal_position, False)
                if not fiscal_position_id:
                    fiscal_position_ids = Fiscal.search([('name','=',fiscal_position)])
                    if fiscal_position_ids:
                        fiscal_position_id = fiscal_position_ids[0].id
                        fiscal_data[fiscal_position] = fiscal_position_id

            pricelist_id = False
            pricelist = order.get('pricelist', False)
            if pricelist:
                pricelist_id = pricelist_data.get(pricelist, False)
                if not pricelist_id:
                    pricelist_ids = PriceList.search([('name','=',pricelist)])
                    if pricelist_ids:
                        pricelist_id = pricelist_ids[0].id
                        pricelist_data[pricelist] = pricelist_id

            line_vals = []
            for pos_line in order.get('order_lines',[]):
                barcode = pos_line.get('barcode', False)
                if barcode:
                    product_id = product_data.get(barcode, False)
                    if not product_id:
                        product_ids = Product.search([('barcode', '=', barcode)])
                        if product_ids:
                            product_id = product_ids[0].id
                            product_data[barcode] = product_id
                product = Product.browse(product_id)
                tax_ids = []
                tax_name = pos_line.get('tax_name',False)
                if tax_name:
                    tax_ids = tax_data.get(tax_name,False)
                    if not tax_ids:
                        taxes = Tax.search([('name','=',tax_name)])
                        if taxes:
                            tax_ids = taxes.ids
                            tax_data[tax_name] = tax_ids

                vals = {
                    'product_id':product_id,
                    'name':product.name,
                    'full_product_name':product.name,
                    'price_unit':pos_line.get('unit_price',0.0),
                    'qty':pos_line.get('qty',0.0),
                    'product_uom_id':product.uom_id.id,
                    'product_uom':product.uom_id.id,
                    'price_subtotal':pos_line.get('subtotal_wo_tax',0.0),
                    'price_subtotal_incl':pos_line.get('subtotal',0.0),
                    'discount':pos_line.get('disc_perc',0.0),
                    'tax_ids':[(6, 0, tax_ids)],
                    'tax_ids_after_fiscal_position':[(6, 0, tax_ids)],
                    'company_id':1,
                }
                line_vals.append((0, 0, vals))

            # Payment lines
            payment_vals = []
            for payment_line in order.get('payment_lines', []):
                payment_method_id = False
                payment_method = payment_line.get('payment_method','')
                if payment_method:
                    payment_method_id = payment_data.get(payment_method,False)
                    if not payment_method_id:
                        payment_method_ids = PaymentMethod.search([('name','=',payment_method)])
                        if payment_method_ids:
                            payment_method_id = payment_method_ids[0].id
                            payment_data[payment_method] = payment_method_id

                vals = {
                    'name':payment_line.get('payment_name',''),
                    'amount':payment_line.get('amount',''),
                    'payment_date':payment_line.get('payment_date',''),
                    'payment_method_id':payment_method_id,
                }
                payment_vals.append((0, 0, vals))
                # payment_vals.append(vals)


            if config.sequence_line_id:
                order_name = config.sequence_line_id._next()

            order_vals = {
                # 'name':order.get('order_number'),
                'name':order_name,
                'user_id':user_id,
                'session_id':order.get('session_id'),
                'pos_reference':order.get('pos_reference',''),
                'partner_id':partner_id,
                'date_order':order.get('date_order',''),
                'fiscal_position_id':fiscal_position_id,
                'pricelist_id':pricelist_id,
                'amount_paid':order.get('paid',0.0),
                'amount_total':order.get('total',0.0),
                'amount_tax':order.get('taxes',0.0),
                'amount_return':0.0,
                'company_id':1,
                # 'state':'paid',
                'lines':line_vals,
                'payment_ids':payment_vals,
            }
            pos_order_id = Pos.create(order_vals)
            # pos_order_id.state='paid'

            # for payment_line in payment_vals:
            #     pos_order_id.add_payment({
            #         'name':payment_line.get('payment_name',''),
            #         'amount':payment_line.get('amount',''),
            #         'payment_date':payment_line.get('payment_date',''),
            #         'payment_method_id':payment_line.get('payment_method_id',''),
            #         'pos_order_id':pos_order_id.id,
            #     })

            # if pos_order_id._is_pos_order_paid():
            # pos_order_id.action_pos_order_paid()
            pos_order_id.write({'state': 'paid'})
            pos_order_id._create_order_picking()
            pos_order_id._compute_total_cost_in_real_time()

        return True