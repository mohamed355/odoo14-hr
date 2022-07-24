odoo.define('recruitment_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var ajax = require('web.ajax');

var RecDashboard =  AbstractAction.extend({
        template: 'Rec Dashboard',

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardRec','DashboardStages'];
            this.open_hiring = [];
            this.hr_applicant = [];
            this.stages = [];

        }   ,
        start: function() {
            var self = this;
            this.set("title", 'Dashboardn');
            return this._super().then(function() {
                self.render_dashboards();
//                self.render_graphs();

            });
        },

        render_dashboards: function() {
        var self = this;
        _.each(this.dashboards_templates, function(template) {
            self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}));
        });

    },
    willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {

                 return self.fetch_data();

            });
        },

    fetch_data: function() {
        var self = this;
        var def1 =  this._rpc({
                model: 'hr.applicant',
                method: 'get_data',

            }).then(function(result) {
                self.open_hiring = result['open_hiring'];
                self.hr_applicant = result['hr_applicant'];

        });
        var def2 = this._rpc({
                    model: "hr.applicant",
                    method: "get_stages",
                })
                .then(function (result) {
                self.stages = result['stages_list'];
            });

            return $.when(def1,def2);
    },

});


core.action_registry.add('rec_dashboard_tag', RecDashboard);

return RecDashboard;
});