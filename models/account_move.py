# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('project.project', string='Project')
    project_user_id = fields.Many2one(string='Project Manager', related='project_id.user_id', store=True)
