import ast
import base64
import re

from odoo import _, api, fields, models, tools, Command
from odoo.exceptions import UserError
from odoo.tools import email_re


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def action_send_offer(self):
        print('Send Email')
        template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
        template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
        template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
        template = None
        if self.template == 'ksa':
            template = self.env['mail.template'].browse(template_ksa.id).id
        if self.template == 'egy':
            template = self.env['mail.template'].browse(template_egy.id).id
        if self.template == 'saudi':
            template = self.env['mail.template'].browse(template_sa.id).id
        print(template)
        if template:
            ctx = {
                'default_model': 'hr.applicant',
                'default_res_id': self.id,
                'default_use_template': bool(template),
                'default_template_id': template,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'custom_layout': "mail.mail_notification_paynow",
                # 'proforma': sale.env.context.get('proforma', False),
                'force_email': True,
                # 'model_description': sale.with_context(lang=lang).type_name,
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


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def default_template_id(self):
        default = None
        print(self.model)
        if self.model == 'hr.applicant':
            template_ksa = self.env.ref('offer_template.application_ksa_offer_template_ksa')
            template_egy = self.env.ref('offer_template.application_ksa_offer_template_egy')
            template_sa = self.env.ref('offer_template.application_ksa_offer_template_saudi_job')
            app = self.env['hr.applicant'].browse(self.res_id)
            if app.template == 'ksa':
                default = template_ksa.id
            if app.template == 'egy':
                default = template_egy.id
            if app.template == 'saudi':
                default = template_sa.id
            print(default)
        return default

    template_ids = fields.Many2many(comodel_name="mail.template", relation="mailtemplate", column1="mail",
                                    column2="tempalte", string="templates", compute='_compute_template')

    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('id', 'in', template_ids)]", default=default_template_id)

    show_templates = fields.Boolean(string="Show Templates", )

    @api.depends('show_templates')
    def _compute_template(self):
        for record in self:
            print("Yes")
            if self.env.user.has_group('hr_recruitment.group_hr_recruitment_user') and not self.env.user.has_group(
                    'hr_recruitment.group_hr_recruitment_manager'):
                print("Yes Group")

                record.template_ids = self.env['mail.template'].search(
                    [('model', '=', record.model),
                     ('name', 'not in', ['Applicant: Saudi job Offer Template', 'Applicant: Ksa Offer Template',
                                         'Applicant: Egypt Offer Template'])]).ids
            else:
                record.template_ids = self.env['mail.template'].search(
                    [('model', '=', record.model),
                     ]).ids

    def _action_send_mail(self, auto_commit=False):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed. """
        notif_layout = self._context.get('custom_layout')
        # Several custom layouts make use of the model description at rendering, e.g. in the
        # 'View <document>' button. Some models are used for different business concepts, such as
        # 'purchase.order' which is used for a RFQ and and PO. To avoid confusion, we must use a
        # different wording depending on the state of the object.
        # Therefore, we can set the description in the context from the beginning to avoid falling
        # back on the regular display_name retrieved in '_notify_prepare_template_context'.
        model_description = self._context.get('model_description')
        for wizard in self:
            if wizard.attachment_ids and wizard.composition_mode != 'mass_mail' and wizard.template_id:
                if wizard.model == 'hr.applicant':
                    app = self.env['hr.applicant'].browse(wizard.res_id)
                    offer = None
                    if app.hiring_ids:
                        offer = self.env['report.job.offer'].create({
                            'name': app.partner_name,
                            'hiring': app.hiring_ids[0].name,
                            'job_title': app.hiring_ids[0].job_id.name,
                            'location': app.hiring_ids[0].location,
                            'client': app.hiring_ids[0].client.name,
                            'offer_job_title': app.offer_job_id,
                            'offer_date': fields.Datetime.now(),
                            'package_salary': app.package_salary,
                            'housing': app.housing,
                            'basic': app.basic,
                            'transportation': app.transportation,
                        })
                    else:
                        offer = self.env['report.job.offer'].create({
                            'name': app.partner_name,
                            'offer_job_title': app.offer_job_id,
                            'offer_date': fields.Datetime.now(),
                            'package_salary': app.package_salary,
                            'housing': app.housing,
                            'basic': app.basic,
                            'transportation': app.transportation,
                        })
                    if app.proposed_currency:
                        offer.write({'currency_id': app.proposed_currency.id})

                    if app.package_salary != 0:
                        print("Ss")
                    elif app.package_salary == 0:
                        raise UserError("The Packaging Should Be More Than 0")
                        break
            # Duplicate attachments linked to the email.template.
            # Indeed, basic mail.compose.message wizard duplicates attachments in mass
            # mailing mode. But in 'single post' mode, attachments of an email template
            # also have to be duplicated to avoid changing their ownership.
            if wizard.attachment_ids and wizard.composition_mode != 'mass_mail' and wizard.template_id:
                new_attachment_ids = []
                for attachment in wizard.attachment_ids:
                    if attachment in wizard.template_id.attachment_ids:
                        new_attachment_ids.append(
                            attachment.sudo().copy({'res_model': 'mail.compose.message', 'res_id': wizard.id}).id)
                    else:
                        new_attachment_ids.append(attachment.id)
                new_attachment_ids.reverse()
                wizard.write({'attachment_ids': [Command.set(new_attachment_ids)]})

            # Mass Mailing
            mass_mode = wizard.composition_mode in ('mass_mail', 'mass_post')

            ActiveModel = self.env[wizard.model] if wizard.model and hasattr(self.env[wizard.model],
                                                                             'message_post') else self.env[
                'mail.thread']
            if wizard.composition_mode == 'mass_post':
                # do not send emails directly but use the queue instead
                # add context key to avoid subscribing the author
                ActiveModel = ActiveModel.with_context(mail_notify_force_send=False, mail_create_nosubscribe=True)
            # wizard works in batch mode: [res_id] or active_ids or active_domain
            if mass_mode and wizard.use_active_domain and wizard.model:
                res_ids = self.env[wizard.model].search(ast.literal_eval(wizard.active_domain)).ids
            elif mass_mode and wizard.model and self._context.get('active_ids'):
                res_ids = self._context['active_ids']
            else:
                res_ids = [wizard.res_id]

            batch_size = int(self.env['ir.config_parameter'].sudo().get_param('mail.batch_size')) or self._batch_size
            sliced_res_ids = [res_ids[i:i + batch_size] for i in range(0, len(res_ids), batch_size)]

            if wizard.composition_mode == 'mass_mail' or wizard.is_log or (
                    wizard.composition_mode == 'mass_post' and not wizard.notify):  # log a note: subtype is False
                subtype_id = False
            elif wizard.subtype_id:
                subtype_id = wizard.subtype_id.id
            else:
                subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

            for res_ids in sliced_res_ids:
                # mass mail mode: mail are sudo-ed, as when going through get_mail_values
                # standard access rights on related records will be checked when browsing them
                # to compute mail values. If people have access to the records they have rights
                # to create lots of emails in sudo as it is consdiered as a technical model.
                batch_mails_sudo = self.env['mail.mail'].sudo()
                all_mail_values = wizard.get_mail_values(res_ids)
                for res_id, mail_values in all_mail_values.items():
                    if wizard.composition_mode == 'mass_mail':
                        batch_mails_sudo |= self.env['mail.mail'].sudo().create(mail_values)
                    else:
                        post_params = dict(
                            message_type=wizard.message_type,
                            subtype_id=subtype_id,
                            email_layout_xmlid=notif_layout,
                            add_sign=not bool(wizard.template_id),
                            mail_auto_delete=wizard.template_id.auto_delete if wizard.template_id else self._context.get(
                                'mail_auto_delete', True),
                            model_description=model_description)
                        post_params.update(mail_values)
                        if ActiveModel._name == 'mail.thread':
                            if wizard.model:
                                post_params['model'] = wizard.model
                                post_params['res_id'] = res_id
                            if not ActiveModel.message_notify(**post_params):
                                # if message_notify returns an empty record set, no recipients where found.
                                raise UserError(_("No recipient found."))
                        else:
                            ActiveModel.browse(res_id).message_post(**post_params)

                if wizard.composition_mode == 'mass_mail':
                    batch_mails_sudo.send(auto_commit=auto_commit)
