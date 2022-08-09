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
            'change #income_expense_values': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="this_year"){
                    this.onclick_this_year($target.val());
                }else if (value=="this_month"){
                    this.onclick_this_month($target.val());
                }

            },
            'change #source_select': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="lost_last_12months"){
                    this.onclick_source_12months($target.val());
                }else if (value=="lost_last_6months"){
                    this.onclick_source_6months($target.val());
                }else if (value=="lost_last_month"){
                    this.onclick_source_month($target.val());
                }
            },
},
        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardRec','DashboardStages'];
            this.open_hiring = [];
            this.hr_applicant = [];
            this.h_a = [];
            this.h_com = [];

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
//        self.onclick_source_month();
//        self.onclick_source_6months();
//        self.onclick_source_12months();
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
    onclick_this_month: function (ev) {
            var self = this;
            rpc.query({
                model: 'hr.applicant',
                method: 'crm_month',
                args: [],
            })
            .then(function (result) {
                $('#leads_this_year').hide();
                $('#hiring_this_year').hide();
//                $('#exp_rev_this_year').hide();
//                $('#rev_this_year').hide();
//                $('#ratio_this_year').hide();
//                $('#avg_time_this_year').hide();
//                $('#total_revenue_this_year').hide();
//                $('#leads_this_quarter').hide();
//                $('#opp_this_quarter').hide();
//                $('#exp_rev_this_quarter').hide();
//                $('#rev_this_quarter').hide();
//                $('#ratio_this_quarter').hide();
//                $('#avg_time_this_quarter').hide();
//                $('#total_revenue_this_quarter').hide();
//                $('#leads_this_week').hide();
//                $('#opp_this_week').hide();
//                $('#exp_rev_this_week').hide();
//                $('#rev_this_week').hide();
//                $('#ratio_this_week').hide();
//                $('#avg_time_this_week').hide();
//                $('#total_revenue_this_week').hide();
//
                $('#leads_this_month').show();
                $('#hiring_this_month').show();
//                $('#exp_rev_this_month').show();
//                $('#rev_this_month').show();
//                $('#ratio_this_month').show();
//                $('#avg_time_this_month').show();
//                $('#total_revenue_this_month').show();

                $('#leads_this_month').empty();
                $('#hiring_this_month').empty();
//                $('#exp_rev_this_month').empty();
//                $('#rev_this_month').empty();
//                $('#ratio_this_month').empty();
//                $('#avg_time_this_month').empty();
//                $('#total_revenue_this_month').empty();

                $('#leads_this_month').append('<span>' + result.leads + '</span>');
                $('#hiring_this_month').append('<span>' + result.hiring + '</span>');
//                $('#exp_rev_this_month').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev_exp + '</span>');
//                $('#rev_this_month').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev + '</span>');
//                $('#ratio_this_month').append('<span>' + result.record_ratio + '</span>');
//                $('#avg_time_this_month').append('<span>' + result.avg_time  + '&nbspsec' + '</span>');
//                $('#total_revenue_this_month').append('<span>' + result.opportunity_ratio_value + '</span>');
            })
        },
    onclick_this_year: function (ev) {
            var self = this;
            rpc.query({
                model: 'hr.applicant',
                method: 'crm_year',
                args: [],
            })
            .then(function (result) {
//                $('#leads_this_quarter').hide();
//                $('#opp_this_quarter').hide();
//                $('#exp_rev_this_quarter').hide();
//                $('#rev_this_quarter').hide();
//                $('#ratio_this_quarter').hide();
//                $('#avg_time_this_quarter').hide();
//                $('#total_revenue_this_quarter').hide();
                $('#leads_this_month').hide();
                $('#hiring_this_month').hide();
//                $('#exp_rev_this_month').hide();
//                $('#rev_this_month').hide();
//                $('#ratio_this_month').hide();
//                $('#avg_time_this_month').hide();
//                $('#total_revenue_this_month').hide();
//                $('#leads_this_week').hide();
//                $('#opp_this_week').hide();
//                $('#exp_rev_this_week').hide();
//                $('#rev_this_week').hide();
//                $('#ratio_this_week').hide();
//                $('#avg_time_this_week').hide();
//                $('#total_revenue_this_week').hide();

                $('#leads_this_year').show();
                $('#hiring_this_year').show();
//                $('#exp_rev_this_year').show();
//                $('#rev_this_year').show();
//                $('#ratio_this_year').show();
//                $('#avg_time_this_year').show();
//                $('#total_revenue_this_year').show();

                $('#leads_this_year').empty();
                $('#hiring_this_year').empty();
//                $('#exp_rev_this_year').empty();
//                $('#rev_this_year').empty();
//                $('#ratio_this_year').empty();
//                $('#avg_time_this_year').empty();
//                $('#total_revenue_this_year').empty();
//
                $('#leads_this_year').append('<span>' + result.leads + '</span>');
                $('#hiring_this_year').append('<span>' + result.hiring + '</span>');
//                $('#exp_rev_this_year').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev_exp + '</span>');
//                $('#rev_this_year').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev + '</span>');
//                $('#ratio_this_year').append('<span>' + result.record_ratio + '</span>');
//                $('#avg_time_this_year').append('<span>' + result.avg_time + '&nbspsec' + '</span>');
//                $('#total_revenue_this_year').append('<span>' + result.opportunity_ratio_value + '</span>');
            })
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
        onclick_source_12months: function(ev) {
            var self = this;
                rpc.query({
                    model: "hr.applicant",
                    method: "get_sources",
                    args: ['12']
                }).then(function(result){
                    var ctx = document.getElementById("canvas").getContext('2d');
                    // Define the data
                    var lost_reason = result.month // Add data values to array
                    var count = result.count;
                    var myChart = new Chart(ctx, {
                        type: 'horizontalBar',
                        data: {
                            labels: lost_reason,//x axis
                            datasets: [{
                                label: 'Count', // Name the series
                                data: count, // Specify the data values array
                                backgroundColor: '#66aecf',
                                borderColor: '#66aecf',
                                barPercentage: 0.5,
                                barThickness: 6,
                                maxBarThickness: 8,
                                minBarLength: 0,
                                borderWidth: 1, // Specify bar border width
                                type: 'horizontalBar', // Set this data to a line chart
                                fill: false
                            }]
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                },
                            },
                            responsive: true, // Instruct chart js to respond nicely.
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        }
                    });
                });
            },


        onclick_source_6months: function(ev) {
            var self = this;
            rpc.query({
                model: "hr.applicant",
                method: "get_sources",
                args: ['6']
            }).then(function(result){
                var ctx = document.getElementById("canvas").getContext('2d');
                // Define the data
                var lost_reason = result.month // Add data values to array
                var count = result.count;
                var myChart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: lost_reason,//x axis
                        datasets: [{
                            label: 'Count', // Name the series
                            data: count, // Specify the data values array
                            backgroundColor: '#66aecf',
                            borderColor: '#66aecf',
                            barPercentage: 0.5,
                            barThickness: 6,
                            maxBarThickness: 8,
                            minBarLength: 0,
                            borderWidth: 1, // Specify bar border width
                            type: 'horizontalBar', // Set this data to a line chart
                            fill: false
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            });
        },

        onclick_source_month: function(ev) {
            var self = this;
            rpc.query({
                model: "hr.applicant",
                method: "get_sources",
                args: ['1']
            }).then(function(result){
                var ctx = document.getElementById("canvas").getContext('2d');
                // Define the data
                var lost_reason = result.month // Add data values to array
                var count = result.count;
                var myChart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: lost_reason,//x axis
                        datasets: [{
                            label: 'Count', // Name the series
                            data: count, // Specify the data values array
                            backgroundColor: '#66aecf',
                            borderColor: '#66aecf',
                            barPercentage: 0.5,
                            barThickness: 6,
                            maxBarThickness: 8,
                            minBarLength: 0,
                            borderWidth: 1, // Specify bar border width
                            type: 'horizontalBar', // Set this data to a line chart
                            fill: false
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
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
                self.h_a = result['h_a'];
                self.h_com = result['h_com'];

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