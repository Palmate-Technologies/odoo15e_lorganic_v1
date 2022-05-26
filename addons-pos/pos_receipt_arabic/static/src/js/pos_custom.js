odoo.define('pos_receipt_arabic.pos_custom', function(require) {'use strict';

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
    var _super_Orderline = models.Orderline.prototype;

    models.load_fields('res.company',['arabic_name']);
    models.load_fields('product.product',['english_name','arabic_name', 'name_arabic']);

    models.Order = models.Order.extend({
//        export_for_printing: function() {
//            var result = _super_order.export_for_printing.apply(this,arguments);
//            var company = this.pos.company;
//
//            result.company.arabic_name = company.arabic_name;
//            result.name_compressed = result.name.substring(6);
//
//            return result;
//        },


        export_for_printing: function() {
            var result = _super_order.export_for_printing.apply(this,arguments);
            var company = this.pos.company;
            result.company.arabic_name = company.arabic_name;
            result.name_compressed = result.name.substring(6);
//            result.qr_data =this.compute_sa_qr_code(result);
            result.qr_data =this.compute_sa_qr_code(this.company.name, this.company.vat, this.date.isostring, this.total_with_tax, this.total_tax);
            return result;
        },


         compute_sa_qr_code: function(receipt) {

                var company = this.pos.company;
                var name = company.name
                var vat = company.vat || ""
                var date_isostring = receipt.date.isostring
                var amount_total = receipt.total_with_tax.toFixed(2).toString()
                var amount_tax = receipt.total_tax.toFixed(2).toString()


                /* Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
                https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
                */
                const seller_name_enc = this._compute_qr_code_field(1, name);
                const company_vat_enc = this._compute_qr_code_field(2, vat);
                const timestamp_enc = this._compute_qr_code_field(3, date_isostring);
                const invoice_total_enc = this._compute_qr_code_field(4, amount_total.toString());
                const total_vat_enc = this._compute_qr_code_field(5, amount_tax.toString());

                const str_to_encode = seller_name_enc.concat(company_vat_enc, timestamp_enc, invoice_total_enc, total_vat_enc);

                let binary = '';
                for (let i = 0; i < str_to_encode.length; i++) {
                    binary += String.fromCharCode(str_to_encode[i]);
                }
                return btoa(binary);
            },

              _compute_qr_code_field(tag, field) {
                const textEncoder = new TextEncoder();
                const name_byte_array = Array.from(textEncoder.encode(field));
                const name_tag_encoding = [tag];
                const name_length_encoding = [name_byte_array.length];
                return name_tag_encoding.concat(name_length_encoding, name_byte_array);
            },

    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var result = _super_Orderline.export_for_printing.apply(this,arguments);
            result.product_name = this.get_product().english_name;
            result.product_arabic_name = this.get_product().arabic_name;
            return result;
        },
    });

});
