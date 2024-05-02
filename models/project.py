# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models, _
from datetime import timedelta
import base64


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_pss_sent = fields.Boolean('PSS to be Sent')

    def action_pss_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        sale_order = self.env['sale.order'].search([('project_id', '=', self.id)])
        subject_name = str(sale_order.mapped('name')).strip("[]").replace("'", "").replace(",", "")
        template = self.env.ref('studio_customization.project_status_sheet_bca6a6aa-a2d3-40b6-b607-5ba02828b3a2')
        pdf = self.env.ref('studio_customization.project_report_d178c5c5-4dad-47e4-b745-bb7c1cc41720')._render_qweb_pdf(self.ids)[0]
        attachment = self.env['ir.attachment'].create({
            'name': _('PSS - %s - %s.pdf') % (subject_name, fields.Date.today()) if subject_name else _('PSS - %s.pdf') % fields.Date.today(),
            'type': 'binary',
            'datas': base64.b64encode(pdf),
            'res_model': 'mail.message',
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })
        partner_list = self.partner_id.ids
        partner_list.append(self.user_id.partner_id.id)
        ctx = {
            'default_model': 'project.project',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': attachment.ids,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'default_partner_ids': partner_list,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def _send_email_pss_cron(self):
        template = self.env.ref('studio_customization.project_status_sheet_bca6a6aa-a2d3-40b6-b607-5ba02828b3a2')
        pss_projects = self.env['project.project'].search([('is_pss_sent', '=', True)])
        project_dict = {}
        project_dump = self.env['project.project']
        for project in pss_projects:
            equal_projects = pss_projects.filtered(lambda r: r.partner_id == project.partner_id)
            if project.partner_id:
                project_dict[project.partner_id.id] = equal_projects.ids
            if project.user_id:
                project_dict[project.user_id.partner_id.id] = equal_projects.ids
            for partner in project.message_follower_ids.mapped('partner_id'):
                if partner.id not in project_dict.keys():
                    project_dict[partner.id] = equal_projects.ids

        print('\n\n\n-------------project_dict----->>:', project_dict)
        print('\n\n\n\n')
        for member in project_dict:
            projects = self.browse(project_dict[member])
            project_dump |= projects 
            sale_order = self.env['sale.order'].search([('project_id', 'in', projects.ids)])
            subject_name = str(sale_order.mapped('name')).strip("[]").replace("'", "").replace(",", "")
            members = self.env['res.partner'].browse(member)
            pdf_content = self.env.ref('studio_customization.project_report_d178c5c5-4dad-47e4-b745-bb7c1cc41720')._render_qweb_pdf(project_dict[member])[0]
            attachment = self.env['ir.attachment'].create({
                'name': _('PSS - %s - %s.pdf') % (subject_name, fields.Date.today()) if subject_name else _('PSS - %s.pdf') % fields.Date.today(),
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'mail.message',
                'res_id': members.id,
                'mimetype': 'application/pdf'
            })
            email_values = {
                'email_from': members.company_id.partner_id.email_formatted or self.env.user.company_id.email_formatted,
                'email_to': members.email,
                'subject': _('PSS - %s - %s') % (subject_name, fields.Date.today()) if subject_name else _('PSS - %s') % fields.Date.today(),
                'recipient_ids': [Command.link(members.id)],
                'attachment_ids': attachment.ids
            }
            template.send_mail(self.env.user.partner_id.id, force_send=True, notif_layout="mail.mail_notification_paynow", email_values=email_values)

            # for project in projects[0]:
            project[member].ids.message_post(body=_('Dear Customer,<br/><br/>Please find enclosed the Project Status Sheet related to the project you manage : ' 
                '<strong>%s</strong><br/><br/>' 
                'This report gives you an up to date view of the following topics :<br/><br/>' 
                '<ol>'
                '<li>Achievements</li>'
                '<li>Risk and Issues</li>'
                '<li>Next Steps</li>'
                '<li>Escalations (if applicable)</li>'
                '</ol><br/>'
                'If any question or remark, feel free to contact our Project Manager : <strong>%s</strong><br/>'
                'For any escalation on this project, feel free to contact your escalation point of contact : <strong>David Di Graci</strong>') % (project.name, project.user_id.name), 
            subject=_('PSS - %s - %s') % (subject_name, fields.Date.today()) if subject_name else _('PSS - %s') % fields.Date.today(), 
            attachments_ids=attachment.ids, email_layout_xmlid='mail.mail_notification_light')
