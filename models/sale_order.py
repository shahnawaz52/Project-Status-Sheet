# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        return dict(super()._prepare_invoice(), **{
            'project_id': self.project_id.id,
        })

    def _update_project_invoice(self):
        sale_orders = self.search([('project_id', '!=', False)])
        for order in sale_orders:
            invoices = order.order_line.invoice_lines.move_id
            invoices.write({'project_id': order.project_id})
