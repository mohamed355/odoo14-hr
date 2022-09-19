odoo.define('crm_dashboard_module.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var _t = core._t;
var ajax = require('web.ajax');

var PosDashboard =  AbstractAction.extend({
        template: 'Dashboard',
        events: {
//            'click .hiring':'hiring',
//            'click .apps':'apps',
//            'click .stage_click':'stage_click',
            'click .calls':'calls',
            'click .close':'close',
            'click .act':'act',
            'click .meeting':'meeting',
            'click .opp':'opp',
            'click .leads':'leads',
            'click .openopp':'openopp',

            },
        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardOrders','DashboardChart'];
            this.total_lead = [];
            this.total_opp = [];
            this.total_activity = [];
            this.crm_activity_call = [];
            this.recent_activities = [];
            this.get_recent_todo_activities = [];
            this.crm_activity_meeting = [];
            this.get_recent_call_activities = [];
            this.close_to = [];
            this.open_opp = [];
        }   ,
        start: function() {
            var self = this;
            this.set("title", 'Dashboardn');
            return this._super().then(function() {
                self.render_dashboards();
                self.render_graphs();

            });
        },
    render_graphs: function(){
    var self = this;
    self.crm_lead_graph();
    self.render_sales_activity_graph();
    self.funnel_chart();
    },
     funnel_chart: function () {
            rpc.query({
                model: "crm.lead",
                method: "get_lead_stage_data",
            }).then(function (callbacks) {
                Highcharts.chart("container", {
                    chart: {
                        type: "funnel",
                    },
                    title: false,
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                softConnector: true
                            },
                            center: ['45%', '50%'],
                            neckWidth: '40%',
                            neckHeight: '35%',
                            width: '90%',
                            height: '80%'
                        }
                    },
                    series: [ {
                        name: "Number Of Opportunities",
                        data: callbacks,
                    }],
                });
            });
        },
render_sales_activity_graph:function(){
            var self = this
            var ctx = self.$(".activity");
            rpc.query({
                model: "crm.lead",
                method: "get_the_sales_activity",
            }).then(function (arrays) {
                var data = {
                    labels : arrays[1],
                    datasets: [{
                        label: "",
                        data: arrays[0],
                        backgroundColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderWidth: 1
                    },]
                };
         var options = {
                    responsive: true,
                    title: false,
                    legend: {
                        display: true,
                        position: "bottom",
                        labels: {
                            fontColor: "#333",
                            fontSize: 16
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                                display: false,
                            },
                            ticks: {
                                min: 0,
                                display: false,
                            }
                        }]
                    }
                };

                //create Chart class object
                var chart = new Chart(ctx, {
                    type: "doughnut",
                    data: data,
                    options: options
                });
            });
        },
       calls: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Calls"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['activity_type_id.category', '=', "phonecall"],['res_model', '=', "crm.lead"]],
            target: 'current'
        }, options)
    },
     close: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        const date = new Date();
        const first = new Date(date.getFullYear(), date.getMonth(), 1);
        const last = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        console.log(first);

        self.do_action({
            name: _t("Close In Month"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['date_deadline', '>=', first],['date_deadline', '<=', last]],
            target: 'current'
        }, options)
    },
    act: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Crm Activities"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['res_model', '=', "crm.lead"]],
            target: 'current'
        }, options)
    },
    opp: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Opportunity"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['type', '=', "opportunity"]],
            target: 'current'
        }, options)
    },
    openopp: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Open Opportunity"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['type', '=', "opportunity"],['probability', '!=', 100]],
            target: 'current'
        }, options)
    },
    leads: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Leads"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
//                    domain: [['type', '=', "lead"]],
            target: 'current'
        }, options)
    },
    meeting: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Meetings"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
                    domain: [['activity_type_id.category', '=', "meeting"],['res_model', '=', "crm.lead"]],
            target: 'current'
        }, options)
    },
     crm_lead_graph:function(){
            var self = this
            var ctx = self.$(".lost_leads_graph");
            rpc.query({
                model: "crm.lead",
                method: "crm_lead_graph",
            }).then(function (arrays) {
                var data = {
                    labels : arrays[1],
                    datasets: [{
                        label: "",
                        data: arrays[0],
                        backgroundColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderWidth: 1
                    },]
                };
         var options = {
                    responsive: true,
                    title: false,
                    legend: {
                        display: true,
                        position: "bottom",
                        labels: {
                            fontColor: "#333",
                            fontSize: 16
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                                display: false,
                            },
                            ticks: {
                                min: 0,
                                display: false,
                            }
                        }]
                    }
                };

                //create Chart class object
                var chart = new Chart(ctx, {
                    type: "bar",
                    data: data,
                    options: options
                });
            });
        },
        render_dashboards: function() {
        var self = this;
        _.each(this.dashboards_templates, function(template) {
            self.$('.o_pos_dashboard').append(QWeb.render(template, {widget: self}));
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
                model: 'crm.lead',
                method: 'get_data',

            }).then(function(result) {
                self.total_lead = result['total_lead'];
                self.total_opp = result['total_opp'];
                self.total_activity = result['total_activity'];
                self.crm_activity_call = result['crm_activity_call'];
                self.crm_activity_meeting = result['crm_activity_meeting'];
                self.open_opp = result['open_opp'];
                self.close_to = result['close_to'];
        });

         var def2 = this._rpc({
                    model: "crm.lead",
                    method: "get_recent_activities",
                })
                .then(function (result) {
                self.recent_activities = result['activities'];
//                self.get_recent_call_activities = result['activities'];
            });

           var def3 = this._rpc({
                    model: "crm.lead",
                    method: "get_recent_call_activities",
                })
                .then(function (result) {
//                self.recent_activities = result['activities'];
                self.get_recent_call_activities = result['activities'];
            });
            var def4 = this._rpc({
                    model: "crm.lead",
                    method: "get_recent_todo_activities",
                })
                .then(function (result) {
//                self.recent_activities = result['activities'];
                self.get_recent_todo_activities = result['activities'];
            });
//            var def4 = this._rpc({
//                    model: "crm.lead",
//                    method: "get_recent_todo_activities",
//                })
//                .then(function (result) {
//                self.get_recent_call_activities = result['activities'];
////                self.get_recent_call_activities = result['activities'];
//            });
            return $.when(def1,def2,def3,def4);
    },

});


core.action_registry.add('dashboard_tag', PosDashboard);

return PosDashboard;
});