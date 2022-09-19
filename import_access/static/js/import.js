odoo.define('import_access.ImportAccess', function(require) {
"use strict";
const { Component } = owl;
var rpc = require('web.rpc');


const BaseImport = require('base_import.ImportMenu');
var AbstractAction = require('web.AbstractAction');
var config = require('web.config');
var core = require('web.core');
var Dialog = require('web.Dialog');
var session = require('web.session');
var time = require('web.time');
var fieldUtils = require('web.field_utils');

var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var StateMachine = window.StateMachine;
const FavoriteMenu = require('web.FavoriteMenu');
const { useModel } = require('web.Model');

class ImportMenuValidation extends Component {
        constructor() {
            super(...arguments);
            this.model = useModel('searchModel');
        }

        //---------------------------------------------------------------------
        // Handlers
        //---------------------------------------------------------------------

        /**
         * @private
         */
        importRecords() {
        var self = this;
            console.log("Ads")
              rpc.query({
                            model: "hr.applicant",
                            method: "check_access",
                        })
                        .then(function (result) {
                            console.log(result)
                            if (result) {
                            self.action()
        }
        else{
        alert("You Need Access To Import")
        }
            });
            }

         action() {
          const action = {
                type: 'ir.actions.client',
                tag: 'import',
                params: {
                    model: this.model.config.modelName,
                    context: this.model.config.context,
                }
            };
            this.trigger('do-action', {action: action});
         }


        //---------------------------------------------------------------------
        // Static
        //---------------------------------------------------------------------

        /**
         * @param {Object} env
         * @returns {boolean}
         */
        static shouldBeDisplayed(env) {
            return env.view &&
                ['kanban', 'list'].includes(env.view.type) &&
                env.action.type === 'ir.actions.act_window' &&
                !env.device.isMobile &&
                !!JSON.parse(env.view.arch.attrs.import || '1') &&
                !!JSON.parse(env.view.arch.attrs.create || '1');
        }
    }

    ImportMenuValidation.props = {};
    ImportMenuValidation.template = "base_import.ImportRecords";

    FavoriteMenu.registry.add('import-menu', ImportMenuValidation, 1);

    return ImportMenuValidation;


});