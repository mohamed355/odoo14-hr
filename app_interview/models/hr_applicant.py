from odoo import api, fields, models


class HrApp(models.Model):
    _inherit = 'hr.applicant'
    notes = fields.Text(string="Notes", required=False, )
    re_skill = fields.Char(string="Skill1", required=False, readonly=True, default="Relevant educational background")
    skill_re_s = fields.Selection(string="Grade1",
                                  selection=[('rel', 'Related'), ('oc', 'Only courses'), ('nrel', 'Not related')],
                                  required=False, )
    ro_skill = fields.Char(string="Skill2", required=False, readonly=True, default="Related work experience ")
    skill_ro_s = fields.Selection(string="Grade2",
                                  selection=[('per', 'Perfectly matched'), ('mat', 'Matched'), ('poor', 'Poor Match')],
                                  required=False, )
    v_skill = fields.Char(string="Skill3", required=False, readonly=True, default="Verbal communication skills ")
    skill_v_s = fields.Selection(string="Grade3", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    w_skill = fields.Char(string="Skill4", required=False, readonly=True, default="Written communication skills")
    skill_w_s = fields.Selection(string="Grade4", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    a_skill = fields.Char(string="Skill5", required=False, readonly=True, default="Attention to detail ")
    skill_a_s = fields.Selection(string="Grade5", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    t_skill = fields.Char(string="Skill6", required=False, readonly=True, default="Takes initiative")
    skill_t_s = fields.Selection(string="Grade6", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    i_skill = fields.Char(string="Skill7", required=False, readonly=True, default="Integrity")
    skill_i_s = fields.Selection(string="Grade7", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    c_skill = fields.Char(string="Skill8", required=False, readonly=True, default="Cooperation")
    skill_c_s = fields.Selection(string="Grade8", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    s_skill = fields.Char(string="Skill9", required=False, readonly=True, default="Stress tolerance")
    skill_s_s = fields.Selection(string="Grade9", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                             ('not', 'Not observed')], required=False, )
    l_skill = fields.Char(string="Skill10", required=False, readonly=True, default="Learning ability ")
    skill_l_s = fields.Selection(string="Grade10", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                              ('not', 'Not observed')], required=False, )
    in_skill = fields.Char(string="Skill11", required=False, readonly=True, default="Interpersonal skills")
    skill_in_s = fields.Selection(string="Grade11", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                               ('not', 'Not observed')], required=False, )
    pro_skill = fields.Char(string="Skill14", required=False, readonly=True, default="Professional demeanor ")
    skill_pro_s = fields.Selection(string="Grade14", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                                ('not', 'Not observed')], required=False, )
    ca_skill = fields.Char(string="Skill15", required=False, readonly=True, default="Candidate stability")
    skill_ca_s = fields.Selection(string="Grade15", selection=[('ex', 'Excellent'), ('good', 'Good'), ('poor', 'Poor'),
                                                               ('not', 'Not observed')], required=False, )
    att_skill = fields.Char(string="Skill12", required=False, readonly=True, default="Attitude towards his position")
    skill_att_s = fields.Selection(string="Grade12", selection=[('vp', 'Very passionate'), ('pas', 'Passionate'),
                                                                ('poor', 'poor passion'), ('not', 'Not observed')],
                                   required=False, )
    atc_skill = fields.Char(string="Skill13", required=False, readonly=True, default="Attitude towards our company ")
    skill_atc_s = fields.Selection(string="Grade13", selection=[('vi', 'Very interested'), ('in', 'Interested'),
                                                                ('poor', ' Poor interest'), ('not', 'Not observed')],
                                   required=False, )
    interview_date = fields.Datetime(string="Interview Date", required=False, )
    rej_reasons_id = fields.Many2one(comodel_name="hr.applicant.refuse.reason", string="Rejection reasons",
                                     required=False, )
    inter_by = fields.Char(string="Interviewed By", required=False, )
    re_action = fields.Char(string="Recommended Action", required=False, )
