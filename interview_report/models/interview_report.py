from odoo import api, fields, models


class InterviewReport(models.Model):
    _name = 'interview.report'

    name = fields.Char("Code")
    location = fields.Selection(string="Location", selection=[('off', 'Offshore'), ('on', 'Onsite'), ],
                                required=False, readonly=True)
    app_name = fields.Char("Name")
    mobile = fields.Char("Mobile")
    email = fields.Char("Email")
    interviewed_by = fields.Char("Interviewed By")
    date = fields.Datetime("Date/Time")
    job_id = fields.Many2one(comodel_name="hr.job", string="Applying For", required=False, )
    resume = fields.Binary(string="Resume", attachment=True)
    att = fields.Many2one('ir.attachment', string="Att", attachment=True)
    resume_name = fields.Char(string="Resume Name", )
    inter_status = fields.Selection(string="Interview Status",
                                    selection=[('attend', 'Attend'), ('apologized', 'Apologized'),
                                               ('noshow', 'No Show'), ('reschedule', 'Reschedule')],
                                    required=False, )
    rec_action = fields.Selection(string="Recommended Action",
                                  selection=[('passed', 'Passed'), ('passednot', 'Passed not to send'),
                                             ('failed', 'Failed')],
                                  required=False, )
    re_reason = fields.Char(string="Rejection Reason", required=False, )
    notes = fields.Char(string="Notes", required=False, )

    def open(self):
        if self.att:
            return {'type': 'ir.actions.act_url',
                    'url': '/web/content/ir.attachment/' + str(self.att.id) + '/datas?download=true',
                    'target': 'new'}
