# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "PSS Project Status Scheduler",
    'version': '15.0.1.0.3',
    'author': 'Odoo PS',
    'summary': "PSS Project Status Scheduler",
    'description': """Report (Project Status Sheet) Sent on Scheduled Actions
    Task Id = '2859409'""",
    'website': 'www.odoo.com',
    'category': 'Custom Development',
    'depends': ['mail', 'account', 'sale_project'],
    'data': [
        'data/cron.xml',
        'views/account_move_views.xml',
        'views/project_update_views.xml',
        'views/project_view.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
