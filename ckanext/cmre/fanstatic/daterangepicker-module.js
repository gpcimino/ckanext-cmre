this.ckan.module('daterangepicker-module', function ($, _) {
    return {
        initialize: function () {
            console.log("Date initialized for element: ", this.el);

            // Define a new jQuery function to parse parameters from URL
            $.urlParam = function(name) {
                var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
                if (results == null) { return null; } else { return decodeURIComponent(results[1]) || 0; }
            };

            // Pick out relevant parameters
            param_start = $.urlParam('ext_startdate');
            param_end = $.urlParam('ext_enddate');

            $('#clear_range').hide();

            // Populate the datepicker and hidden fields
            if (param_start) {
                $('#datepicker #start').val(moment.utc(param_start).format('YYYY-MM-DD'));
                $('#ext_startdate').val(param_start);
                $('#clear_range').show();
            }
            if (param_end) {
                $('#datepicker #end').val(moment.utc(param_end).format('YYYY-MM-DD'));
                $('#ext_enddate').val(param_end);
                $('#clear_range').show();
            }

            // CKAN Search is submitted after date added!" (Comment Anja 27.4.17)
            var form = $("#dataset-search");
            // CKAN 2.1
            if (!form.length) {
                form = $(".search-form");
            }

            // Add hidden <input> tags #ext_startdate and #ext_enddate, if they don't already exist.// Anja: They are for plugin.py
            if ($("#ext_startdate").length === 0) {
                $('<input type="hidden" id="ext_startdate" name="ext_startdate" />').appendTo(form);
            }
            if ($("#ext_enddate").length === 0) {
                $('<input type="hidden" id="ext_enddate" name="ext_enddate" />').appendTo(form);
            }

            // Add a date-range picker widget to the <input> with id #daterange
            $('#datepicker.input-daterange').datepicker({
                format: "yyyy-mm-dd",
                startView: "month",
                minViewMode: "days",
                startDate: "1990-01-01",
                endDate: "2050-12-31",
                keyboardNavigation: false,
                autoclose: true
            }).on('changeDate', function (ev) {
                    // Bootstrap-daterangepicker calls this function after the user picks a start and end date.

                    // Format the start and end dates into strings in a date format that Solr understands.
                    var v = moment(ev.date);
                    var fs = 'YYYY-MM-DDTHH:mm:ss';
                    ev.preventDefault();
                  	ev.stopPropagation();

                    switch (ev.target.name) {
                        case 'start':
                            // Set the value of the hidden <input id="ext_startdate"> to the chosen start date.
                            if (ev.date) {
                                $('#ext_startdate').val(v.format(fs) + 'Z');
                            } else {
                                //$('#ext_startdate').val('');
                            }
                            console.log("start event");
                            break;
                        case 'end':
                            // Set the value of the hidden <input id="ext_enddate"> to the chosen end date.
                            if (ev.date) {
                                $('#ext_enddate').val(v.format(fs) + 'Z');
                                // $('#ext_enddate').val(v.add('y', 1).subtract('s', 1).format(fs) + 'Z');
                            } else {
                              //  $('#ext_enddate').val('');
                            }
                            console.log("end event");

                            break;
                    }

                    // Submit the <form id="dataset-search">.
                  //  if (  $('#ext_startdate').val() != ''  &&  $('#ext_enddate').val() != '' )
                      form.submit();
            });
        }
    }
});
