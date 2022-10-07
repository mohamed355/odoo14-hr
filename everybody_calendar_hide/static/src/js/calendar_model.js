odoo.define('everybody_calendar_hide.everybodycalendarhide', function (require) {
    'use strict';

    var Context = require('web.Context');
    var fieldUtils = require('web.field_utils');
     var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var Calendar = require('web.CalendarModel');
    var web_client = require('web.web_client');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;

    Calendar.include({
async _calendarEventByAttendee(eventsData) {
            const self = this;
            let eventsDataByAttendee = [];
            const attendeeFilters = self.loadParams.filters.partner_ids;
            const everyoneFilter = attendeeFilters && (attendeeFilters.filters.find(f => f.value === "all") || {}).active || false;
            const attendeeIDs = attendeeFilters && _.filter(attendeeFilters.filters.map(partner => partner.value !== 'all' ? partner.value : false), id => id !== false);
            const eventIDs = eventsData.map(event => event.id);
            // Fetch the attendees' info from the partners selected in the filter to display the events
            this.attendees = await self._rpc({
                model: 'res.partner',
                method: 'get_attendee_detail',
                args: [attendeeIDs, eventIDs],
            });
            console.log(this.attendees)
            if (!everyoneFilter) {
                const currentPartnerId = this.getSession().partner_id;
                eventsData.forEach(event => {
                    const attendees = event.record.partner_ids && event.record.partner_ids.length ? event.record.partner_ids : [event.record.partner_id[0]];
                    // Get the list of partner_id corresponding to active filters present in the current event
                    const attendees_filtered = attendeeFilters.filters.reduce((acc, filter) => {
                        if (filter.active && attendees.includes(filter.value)) {
                            acc.push(filter.value);
                        }
                        return acc;
                    }, []);

                    // Create Event data for each attendee found
                    attendees_filtered.forEach(attendee => {
                        let e = $.extend(true, {}, event);
                        e.attendee_id = attendee;
                        const attendee_info = self.attendees.find(a => a.id === attendee && a.event_id === e.record.id);
                        if (attendee_info) {
                            e.record.attendee_status = attendee_info.status;
                            e.record.is_alone = attendee_info.is_alone;
                            // check if this event data corresponds to the current partner
                            e.record.is_current_partner = currentPartnerId === attendee_info.id;
                        }
                        eventsDataByAttendee.push(e);
                    });
                });
            } else {
                eventsData.forEach(event => {
                    const attendee_info = self.attendees.find(a => a.id === self.getSession().partner_id && a.event_id === event.record.id);
                    if (attendee_info) {
                        event.record.is_alone = attendee_info.is_alone;
                    }
                });
            }
            console.log(eventsDataByAttendee)
            return eventsDataByAttendee.length ? eventsDataByAttendee : eventsData;
        },

           _loadFilter: function (filter) {
        if (!filter.write_model) {
            return Promise.resolve();
        }

        var field = this.fields[filter.fieldName];
        var fields = [filter.write_field];
        if (filter.filter_field) {
            fields.push(filter.filter_field);
        }
        return this._rpc({
                model: filter.write_model,
                method: 'search_read',
                domain: [["user_id", "=", session.uid]],
                fields: fields,
            })
            .then(function (res) {
                var records = _.map(res, function (record) {
                    var _value = record[filter.write_field];
                    var value = _.isArray(_value) ? _value[0] : _value;
                    var f = _.find(filter.filters, function (f) {return f.value === value;});
                    var formater = fieldUtils.format[_.contains(['many2many', 'one2many'], field.type) ? 'many2one' : field.type];
                    // By default, only current user partner is checked.
                    return {
                        'id': record.id,
                        'value': value,
                        'label': formater(_value, field),
                        'active': (f && f.active) || (filter.filter_field && record[filter.filter_field]),
                    };
                });
                records.sort(function (f1,f2) {
                    return _.string.naturalCmp(f2.label, f1.label);
                });

                // add my profile
                if (field.relation === 'res.partner' || field.relation === 'res.users') {
                    var value = field.relation === 'res.partner' ? session.partner_id : session.uid;
                    var me = _.find(records, function (record) {
                        return record.value === value;
                    });
                    if (me) {
                        records.splice(records.indexOf(me), 1);
                    } else {
                        var f = _.find(filter.filters, function (f) {return f.value === value;});
                        me = {
                            'value': value,
                            'label': session.name,
                            'active': !f || f.active,
                        };
                    }
                    records.unshift(me);
                }
                                var userme = new Array()

                var result = rpc.query({
                    model: "calendar.event",
                    method: "check_group_every",
                })
                .then(function (result) {
                    console.log(result)
                    if (result) {
                     userme.push({
                    'value': 'all',
                    'label': field.relation === 'res.users' ? _t("Everybody's calendars") : _t("Everything"),
                    'active': filter.all,
                });

}
                else {
                    console.log("No Access")
                }
    });
                var me = _.find(records, function (record) {
                        return record.label === session.name;
                    });
                records.push(me)
                userme.push(me)
                console.log(userme)
                filter.filters = userme;

                console.log(records)
                console.log(me)


            });
    },
});



    });
