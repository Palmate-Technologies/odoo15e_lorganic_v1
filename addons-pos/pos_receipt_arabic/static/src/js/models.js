odoo.define('pos_receipt_arabic.models', function (require) {
"use strict";

var models = require('point_of_sale.models');

    var models = require('point_of_sale.models');
    models.load_fields('product.product', ['name_arabic']);

    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var result = _super_Orderline.export_for_printing.apply(this,arguments);
            result.product_name = this.get_product().display_name;
            result.product_arabic_name = this.get_product().name_arabic;
            return result;
        },
    });

});