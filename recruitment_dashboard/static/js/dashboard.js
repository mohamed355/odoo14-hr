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
                    this.onclick_this_year($target.val()),
                    this.get_act_don_year($target.val()),
                    this.get_sources_year($target.val()),
                    this.get_job_year($target.val()),
                    this.onclick_get_s_year($target.val());
                }else if (value=="this_month"){
                    this.onclick_this_month($target.val()),
                    this.onclick_get_s_month($target.val());
                    this.get_act_don_month($target.val());
                    this.get_sources_year($target.val());
                    this.get_job_month($target.val());
                }else if (value=="this_quarter"){
                    this.onclick_this_quarter($target.val());
                    this.get_sources_quarter($target.val());
                    this.get_act_don_quarter($target.val());
                    this.get_job_quarter($target.val());
                    this.onclick_get_s_quarter($target.val());
                }else if (value=="all"){
                    this.onclick_get_s_all($target.val());
                    this.get_job_all($target.val());
                    this.get_act_don_all($target.val());
                    this.get_sources_all($target.val());
                    this.onclick_this_all($target.val());
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
            this.app_3 = [];
            this.app_4 = [];
//            this.stages_year = [];

        },


        onclick_toggle_two: function(ev) {
            this.get_stages_this_year(ev);
//            this.onclick_income_last_year(ev);
//            this.onclick_income_this_month(ev);
    },
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
//        self.get_s();
//        self.get_sources();
//        self.get_job();
//        self.get_act_don();
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
    onclick_this_quarter: function (ev) {
       var self = this;
            rpc.query({
                model: 'hr.applicant',
                method: 'crm_quarter',
                args: [],
            })
            .then(function (result) {
               $('#leads_this_month').hide();
                $('#hiring_this_month').hide();
                $('#leads_this_year').hide();
                $('#hiring_this_year').hide();
                $('#h_a_this_year').hide();
                $('#h_com_this_year').hide();
                $('#app_3_this_year').hide();
                $('#app_4_this_year').hide();
                $('#h_a_this_month').hide();
                $('#h_com_this_month').hide();
                $('#app_3_this_month').hide();
                $('#app_4_this_month').hide();
 $('#leads_this_all').hide();
                $('#hiring_this_all').hide();
                 $('#h_a_this_all').hide();
                $('#h_com_this_all').hide();
                $('#app_3_this_all').hide();
                $('#app_4_this_all').hide();

                $('#leads_this_quarter').show();
                $('#hiring_this_quarter').show();
                $('#h_a_this_quarter').show();
                $('#h_com_this_quarter').show();
                $('#app_3_this_quarter').show();
                $('#app_4_this_quarter').show();
//                $('#exp_rev_this_quarter').show();
//                $('#rev_this_quarter').show();
//                $('#ratio_this_quarter').show();
//                $('#avg_time_this_quarter').show();
//                $('#total_revenue_this_quarter').show();

                $('#leads_this_quarter').empty();
                $('#hiring_this_quarter').empty();
                 $('#h_a_this_quarter').empty();
                $('#h_com_this_quarter').empty();
                $('#app_3_this_quarter').empty();
                $('#app_4_this_quarter').empty();
//                $('#exp_rev_this_quarter').empty();
//                $('#rev_this_quarter').empty();
//                $('#ratio_this_quarter').empty();
//                $('#avg_time_this_quarter').empty();
//                $('#total_revenue_this_quarter').empty();

                $('#leads_this_quarter').append('<span>' + result.leads + '</span>');
                $('#hiring_this_quarter').append('<span>' + result.hiring + '</span>');
                $('#h_a_this_quarter').append('<span>' + result.h_a + '</span>');
                $('#h_com_this_quarter').append('<span>' + result.h_com + '</span>'+ '%');
                $('#app_3_this_quarter').append('<span>' + result.app_3 + '</span>'+ '%');
                $('#app_4_this_quarter').append('<span>' + result.app_4 + '</span>'+ '%');
//                $('#exp_rev_this_quarter').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev_exp + '</span>');
//                $('#rev_this_quarter').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev + '</span>');
//                $('#ratio_this_quarter').append('<span>' + result.record_ratio + '</span>');
//                $('#avg_time_this_quarter').append('<span>' + result.avg_time  + '&nbspsec' + '</span>');
//                $('#total_revenue_this_quarter').append('<span>' + result.opportunity_ratio_value + '</span>');
            })
        },

     onclick_this_all: function (ev) {
       var self = this;
            rpc.query({
                model: 'hr.applicant',
                method: 'get_data',
                args: [],
            })
            .then(function (result) {
               $('#leads_this_month').hide();
                $('#hiring_this_month').hide();
                $('#leads_this_year').hide();
                $('#hiring_this_year').hide();
                $('#h_a_this_year').hide();
                $('#h_com_this_year').hide();
                $('#app_3_this_year').hide();
                $('#app_4_this_year').hide();
                $('#h_a_this_month').hide();
                $('#h_com_this_month').hide();
                $('#app_3_this_month').hide();
                $('#app_4_this_month').hide();
                $('#leads_this_quarter').hide();
                $('#hiring_this_quarter').hide();
                $('#h_a_this_quarter').hide();
                $('#h_com_this_quarter').hide();
                $('#app_3_this_quarter').hide();
                $('#app_4_this_quarter').hide();
//                $('#exp_rev_this_quarter').show();
//                $('#rev_this_quarter').show();
//                $('#ratio_this_quarter').show();
//                $('#avg_time_this_quarter').show();
//                $('#total_revenue_this_quarter').show();
                $('#leads_this_all').show();
                $('#hiring_this_all').show();
                 $('#h_a_this_all').show();
                $('#h_com_this_all').show();
                $('#app_3_this_all').show();
                $('#app_4_this_all').show();

                $('#leads_this_all').empty();
                $('#hiring_this_all').empty();
                 $('#h_a_this_all').empty();
                $('#h_com_this_all').empty();
                $('#app_3_this_all').empty();
                $('#app_4_this_all').empty();
//                $('#exp_rev_this_quarter').empty();
//                $('#rev_this_quarter').empty();
//                $('#ratio_this_quarter').empty();
//                $('#avg_time_this_quarter').empty();
//                $('#total_revenue_this_quarter').empty();

                $('#leads_this_all').append('<span>' + result.hr_applicant + '</span>');
                $('#hiring_this_all').append('<span>' + result.open_hiring + '</span>');
                $('#h_a_this_all').append('<span>' + result.h_a + '</span>');
                $('#h_com_this_all').append('<span>' + result.h_com + '</span>'+ '%');
                $('#app_3_this_all').append('<span>' + result.app_3 + '</span>'+ '%');
                $('#app_4_this_all').append('<span>' + result.app_4 + '</span>'+ '%');
//                $('#exp_rev_this_quarter').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev_exp + '</span>');
//                $('#rev_this_quarter').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev + '</span>');
//                $('#ratio_this_quarter').append('<span>' + result.record_ratio + '</span>');
//                $('#avg_time_this_quarter').append('<span>' + result.avg_time  + '&nbspsec' + '</span>');
//                $('#total_revenue_this_quarter').append('<span>' + result.opportunity_ratio_value + '</span>');
            })
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
                 $('#leads_this_quarter').hide();
                $('#hiring_this_quarter').hide();
                $('#h_a_this_year').hide();
                $('#h_com_this_year').hide();
                $('#app_3_this_year').hide();
                $('#app_4_this_year').hide();
                $('#h_a_this_quarter').hide();
                $('#h_com_this_quarter').hide();
                $('#app_3_this_quarter').hide();
                $('#app_4_this_quarter').hide();
                 $('#leads_this_all').hide();
                $('#hiring_this_all').hide();
                 $('#h_a_this_all').hide();
                $('#h_com_this_all').hide();
                $('#app_3_this_all').hide();
                $('#app_4_this_all').hide();

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
                $('#h_a_this_month').show();
                $('#h_com_this_month').show();
                $('#app_3_this_month').show();
                $('#app_4_this_month').show();
//                $('#exp_rev_this_month').show();
//                $('#rev_this_month').show();
//                $('#ratio_this_month').show();
//                $('#avg_time_this_month').show();
//                $('#total_revenue_this_month').show();

                $('#leads_this_month').empty();
                $('#hiring_this_month').empty();
                $('#h_a_this_month').empty();
                $('#h_com_this_month').empty();
                $('#app_3_this_month').empty();
                $('#app_4_this_month').empty();
//                $('#exp_rev_this_month').empty();
//                $('#rev_this_month').empty();
//                $('#ratio_this_month').empty();
//                $('#avg_time_this_month').empty();
//                $('#total_revenue_this_month').empty();

                $('#leads_this_month').append('<span>' + result.leads + '</span>');
                $('#hiring_this_month').append('<span>' + result.hiring + '</span>');
                $('#h_a_this_month').append('<span>' + result.h_a + '</span>');
                $('#h_com_this_month').append('<span>' + result.h_com + '</span>' + '%');
                $('#app_3_this_month').append('<span>' + result.app_3 + '</span>'+ '%');
                $('#app_4_this_month').append('<span>' + result.app_4 + '</span>'+ '%');
//                $('#exp_rev_this_month').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev_exp + '</span>');
//                $('#rev_this_month').append('<span>' + self.monthly_goals[2] + '&nbsp' + result.record_rev + '</span>');
//                $('#ratio_this_month').append('<span>' + result.record_ratio + '</span>');
//                $('#avg_time_this_month').append('<span>' + result.avg_time  + '&nbspsec' + '</span>');
//                $('#total_revenue_this_month').append('<span>' + result.opportunity_ratio_value + '</span>');
            })
        },
//    onclick_toggle_two: function(ev) {
//        this.onclick_income_this_year(ev);
////        this.onclick_income_last_year(ev);
////        this.onclick_income_this_month(ev);
//    },
    get_stages_this_year: function(ev) {
//        ev.stopPropagation();
//        ev.preventDefault();
        var selected = $('.btn.btn-tool.income');
        var data = $(selected[0]).data();
        var posted = false;

        rpc.query({
                model: 'hr.applicant',
                method: 'get_stages_this_year',
                args: [],

            })
            .then(function(result) {

//                $('#net_profit_current_months').hide();
//                $('#net_profit_last_year').hide();
                $('#net_profit_this_year').show();

                var ctx = document.getElementById("canvas").getContext('2d');

                // Define the data
                var income = result.income; // Add data values to array
//                    var expense = result.expense;
                var profit = result.profit;

                var labels = result.month; // Add labels to array


                if (window.myCharts != undefined)
                    window.myCharts.destroy();
                window.myCharts = new Chart(ctx, {
                    //var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Months', // Name the series
                                data: profit, // Specify the data values array
                                backgroundColor: '#0bd465',
                                borderColor: '#0bd465',

                                borderWidth: 1, // Specify bar border width
                                type: 'bar', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
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
                    }
                });

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
                $('#h_a_this_month').hide();
                $('#h_com_this_month').hide();
                $('#app_3_this_month').hide();
                $('#app_4_this_month').hide();
                $('#leads_this_month').hide();
                $('#hiring_this_month').hide();
                 $('#leads_this_quarter').hide();
                $('#hiring_this_quarter').hide();
                $('#h_a_this_quarter').hide();
                $('#h_com_this_quarter').hide();
                $('#app_3_this_quarter').hide();
                $('#app_4_this_quarter').hide();
                 $('#leads_this_all').hide();
                $('#hiring_this_all').hide();
                 $('#h_a_this_all').hide();
                $('#h_com_this_all').hide();
                $('#app_3_this_all').hide();
                $('#app_4_this_all').hide();

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
                $('#h_a_this_year').show();
                $('#h_com_this_year').show();
                $('#app_3_this_year').show();
                $('#app_4_this_year').show();
                $('#app_4_this_stage').show();
//                $('#exp_rev_this_year').show();
//                $('#rev_this_year').show();
//                $('#ratio_this_year').show();
//                $('#avg_time_this_year').show();
//                $('#total_revenue_this_year').show();

                $('#leads_this_year').empty();
                $('#hiring_this_year').empty();
                $('#h_a_this_year').empty();
                $('#h_com_this_year').empty();
                $('#app_3_this_year').empty();
                $('#app_4_this_year').empty();
                                $('#app_4_this_stage').empty();

//                $('#exp_rev_this_year').empty();
//                $('#rev_this_year').empty();
//                $('#ratio_this_year').empty();
//                $('#avg_time_this_year').empty();
//                $('#total_revenue_this_year').empty();
//
                $('#leads_this_year').append('<span>' + result.leads + '</span>');
                $('#hiring_this_year').append('<span>' + result.hiring + '</span>');
                $('#h_a_this_year').append('<span>' + result.h_a + '</span>');
                $('#h_com_this_year').append('<span>' + result.h_com + '</span>'+ '%');
                $('#app_3_this_year').append('<span>' + result.app_3 + '</span>'+ '%');
                $('#app_4_this_year').append('<span>' + result.app_4 + '</span>'+ '%');
//                self.stages_year.append(result.stages_list);
//                $('#app_4_this_stage').append(result.app_4_this_stage);
                 self.stages_year = result['stages_list'];

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


    onclick_get_s_all:function(){
            var self = this
            var ctx = self.$(".get_s");
            rpc.query({
                model: "hr.applicant",
                method: "get_recruiter_all",
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
         onclick_get_s_year:function(){
            var self = this
            var ctx = self.$(".get_s");
            rpc.query({
                model: "hr.applicant",
                method: "get_recruiter_year",
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
        onclick_get_s_month:function(){
            var self = this
            var ctx = self.$(".get_s");
            rpc.query({
                model: "hr.applicant",
                method: "get_recruiter_month",
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
        onclick_get_s_quarter:function(){
            var self = this
            var ctx = self.$(".get_s");
            rpc.query({
                model: "hr.applicant",
                method: "get_recruiter_quarter",
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
        get_act_don_year:function(){
            var self = this
            var ctx = self.$(".get_act_don");
            rpc.query({
                model: "hr.applicant",
                method: "get_act_don_year",
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
        get_act_don_all:function(){
            var self = this
            var ctx = self.$(".get_act_don");
            rpc.query({
                model: "hr.applicant",
                method: "get_act_don_all",
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
        get_act_don_quarter:function(){
            var self = this
            var ctx = self.$(".get_act_don");
            rpc.query({
                model: "hr.applicant",
                method: "get_act_don_quarter",
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
        get_act_don_month:function(){
            var self = this
            var ctx = self.$(".get_act_don");
            rpc.query({
                model: "hr.applicant",
                method: "get_act_don_month",
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

         get_job_year:function(){
            var self = this
            var ctx = self.$(".get_jobs");
            rpc.query({
                model: "hr.applicant",
                method: "get_jobs_year",
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
        get_job_all:function(){
            var self = this
            var ctx = self.$(".get_jobs");
            rpc.query({
                model: "hr.applicant",
                method: "get_jobs_all",
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
        get_job_quarter:function(){
            var self = this
            var ctx = self.$(".get_jobs");
            rpc.query({
                model: "hr.applicant",
                method: "get_jobs_quarter",
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
        get_job_month:function(){
            var self = this
            var ctx = self.$(".get_jobs");
            rpc.query({
                model: "hr.applicant",
                method: "get_jobs_month",
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
        get_sources_year:function(){
            var self = this
            var ctx = self.$(".get_sources");
            rpc.query({
                model: "hr.applicant",
                method: "get_sources_year",
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
        get_sources_all:function(){
            var self = this
            var ctx = self.$(".get_sources");
            rpc.query({
                model: "hr.applicant",
                method: "get_sources_all",
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
        get_sources_quarter:function(){
            var self = this
            var ctx = self.$(".get_sources");
            rpc.query({
                model: "hr.applicant",
                method: "get_sources_quarter",
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
        get_sources_month:function(){
            var self = this
            var ctx = self.$(".get_sources");
            rpc.query({
                model: "hr.applicant",
                method: "get_sources_month",
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
                self.app_3 = result['app_3'];
                self.app_4 = result['app_4'];

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