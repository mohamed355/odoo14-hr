odoo.define('recruitment_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var _t = core._t;
var rpc = require('web.rpc');
var ajax = require('web.ajax');

var RecDashboard =  AbstractAction.extend({
        template: 'Rec Dashboard',
        events: {
            'click .hiring':'hiring',
            'click .apps':'apps',
            'click .stage_click':'stage_click',
            'click .act':'act',

            },
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
                self.render_graphs();
//                self.render_graphs();

            });
        },
    render_graphs: function(){
        var self = this;
        self.get_s();
        self.get_sources();
        self.get_job();
        self.get_act_don();
        },

    hiring: function(e){
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Hiring Requests"),
            type: 'ir.actions.act_window',
            res_model: 'hiring.request',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
//                    domain: [['amount_total', '<', 0.0]],
            target: 'current'
        }, options)



    },
    apps: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Applications"),
            type: 'ir.actions.act_window',
            res_model: 'hr.applicant',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
//                    domain: [['amount_total', '<', 0.0]],
            target: 'current'
        }, options)
    },
    stage_click: function(x){
        var self = this;
        x.stopPropagation();
        x.preventDefault();
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        self.do_action({
            name: _t("Stages"),
            type: 'ir.actions.act_window',
            res_model: 'hr.recruitment.stage',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
//                    domain: [['amount_total', '<', 0.0]],
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
            name: _t("Activities"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
//                    domain: [['amount_total', '<', 0.0]],
            target: 'current'
        }, options)
    },

    get_s:function(){
            var self = this
            var ctx = self.$(".get_s");
            rpc.query({
                model: "hr.applicant",
                method: "get_recruiter",
            }).then(function (arrays) {
            var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Applications",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };
        var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "",
              fontSize: 18,
              fontColor: "#111"
            },
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
                ticks: {
                  min: 0
                }
              }]
            }
          };

                //create Chart class object
                var chart = new Chart(ctx, {
                    type: "horizontalBar",
                    data: data,
                    options: options
                });
            });
        },
        get_act_don:function(){
            var self = this
            var ctx = self.$(".get_act_don");
            rpc.query({
                model: "hr.applicant",
                method: "get_act_don",
            }).then(function (arrays) {
            var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Activities",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
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
         get_job:function(){
            var self = this
            var ctx = self.$(".get_jobs");
            rpc.query({
                model: "hr.applicant",
                method: "get_jobs",
            }).then(function (arrays) {
            var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Applications",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };
         var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "",
              fontSize: 18,
              fontColor: "#111"
            },
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
                ticks: {
                  min: 0
                }
              }]
            }
          };

                //create Chart class object
                var chart = new Chart(ctx, {
                    type: "horizontalBar",
                    data: data,
                    options: options
                });
            });
        },
        get_sources:function(){
            var self = this
            var ctx = self.$(".get_sources");
            rpc.query({
                model: "hr.applicant",
                method: "get_sources",
            }).then(function (arrays) {
            var data = {
            labels: arrays[1],
            datasets: [
              {
                label: "Applications",
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
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