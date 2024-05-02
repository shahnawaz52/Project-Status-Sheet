# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        return dict(super()._prepare_invoice_values(order, name, amount, so_line), **{
            'project_id': order.project_id.id,
        })
