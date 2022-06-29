from odoo import api, fields, models, Command
from collections import defaultdict
from  datetime import date,datetime

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )
    lead_id = fields.Many2one(comodel_name="crm.lead", string="Leads", required=False, )
    date_from = fields.Datetime(string="Date From", required=True,default=datetime.today().strftime('%Y-%m-%d 02:00:00'))
    date_to = fields.Datetime(string="Date To", required=True, default=datetime.today().strftime('%Y-%m-%d 09:00:00'))
    activity_type = fields.Selection(string="Type", selection=[('draft', 'Draft'), ('done', 'Done'), ], required=False, default='draft' )

    @api.onchange('partner_id','opportunity_id','lead_id')
    def onchange_fields_filter(self):
        if self.partner_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','res.partner')],limit=1).id
            self.res_id = self.partner_id.id
        if self.opportunity_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id
            self.res_id = self.opportunity_id.id
        if self.lead_id:
            self.res_model_id = self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id
            self.res_id = self.lead_id.id

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.chaining_type == 'trigger':
                vals = activity.with_context(activity_previous_deadline=activity.date_deadline)._prepare_next_activity_values()
                next_activities_values.append(vals)

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[Command.link(attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )

            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message

        next_activities = self.env['mail.activity'].create(next_activities_values)
        # self.unlink()  # will unlink activity, dont access `self` after that
        self.activity_type = 'done'

        return messages, next_activities
