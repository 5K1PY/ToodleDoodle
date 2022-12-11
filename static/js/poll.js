var pollViewActive = true;
$(function() {
    var $this = $(this);

    // constants
    const AVAILABLE = "✅";
    const NOT_PREFERED = "(✔️)";

    const TRANSPOSE_TABLES_TAG = 'transpose-tables';
    const INTERVAL_MODE_TAG = 'interval-mode';
    const WEIGHTS_TAG = 'weights';
    const BUTTON_TAG = 'buttons';
    const SETTINGS = {
        't': TRANSPOSE_TABLES_TAG,
        'i': INTERVAL_MODE_TAG,
        'w': WEIGHTS_TAG,
        'b': BUTTON_TAG
    };

    // prepare values for interval mode
    var options = [];
    for (var i=0;; i++) {
        var option = $this.find(`#options-${i}`);
        if (option.val() === undefined) {
            break;
        }
        options.push(option.val());
    }

    // interval mode
    function interaval_update() {
        var i = parseInt($(this).attr('id').match(/^options-(\d+)/)[1]);
        if ($this.find(`#${INTERVAL_MODE_TAG}`).is(":checked")) {
            if (i + 1 < options.length && options[i] === options[i+1]) {
                if (enable_interval) {
                    enable_interval = false;
                    $this.find(`#options-${i+1}`).val(this.value).change();
                    enable_interval = true;
                } else {
                    $this.find(`#options-${i+1}`).val(this.value).change();
                }
            }
        }
        options[i] = this.value;
    }
    $this.find('.options-select').change(interaval_update);

    function transpose_tables() {
        $this.find('.options-buttons').each(function () {
            var classes = $(this).attr('class');
            if (classes.includes('btn-group-vertical')) {
                $(this).attr('class', classes.replace('btn-group-vertical', 'btn-group'));
            } else {
                $(this).attr('class', classes.replace('btn-group', 'btn-group-vertical'));
            }
        })
        $this.find(".table").each(function () {
            var $table = $(this);
            var new_table = [];
            var column_i = [];
            $table.find("tr").each(function() {
                column_i.push(0);
            });
            var column = 0;
            $table.find("tr").each(function() {
                $(this).find("th, td").each(function() {
                    var colspan = $(this).attr('colspan');
                    colspan = colspan ? parseInt(colspan) : 1;
                    var rowspan = $(this).attr('rowspan');
                    rowspan = rowspan ? parseInt(rowspan) : 1;
                    $(this).attr('rowspan', colspan);
                    $(this).attr('colspan', rowspan);

                    while (new_table.length <= column_i[column]) {
                        new_table.push($("<tr></tr>"));
                    }
                    new_table[column_i[column]].append($(this));
                    column_i[column] += colspan;
                    for (var i=1; i<rowspan; i++) {
                        column_i[column+i]++;
                    }
                });
                column++;
            });
            $table.find("tr").remove();
            $.each(new_table, function(){
                $table.append(this);
            });
        });
    }
    $this.find(`#${TRANSPOSE_TABLES_TAG}`).change(transpose_tables);

    // show / hide weights
    function toggle_weights() {
        if ($this.find(`#${WEIGHTS_TAG}`).is(":checked")) {
            $this.find(".edit-button").hide();
            $this.find(".delete-button").hide();
            $this.find(".weight").show();
        } else {
            $this.find(".edit-button").show();
            $this.find(".delete-button").show();
            $this.find(".weight").hide();
        }
    }
    $this.find(".weight").hide();
    $this.find(`#${WEIGHTS_TAG}`).change(toggle_weights);

    var locks = Array($this.find(".option-time").length).fill(false);
    var enable_interval = true;
    // sync option between select menus and buttons
    function optionsync(ev) {
        var match = $(this).attr('id').match(/^(options-(\d+))/);
        var [bare_id, id_num] = [match[1], match[2]];
        if (locks[id_num]) {
            return;
        }
        locks[id_num] = true;

        var new_val = (this.value || $(this).find(':checked').next().text());
        if (enable_interval) {
            $this.find(`#${bare_id}`).val(new_val).each(interaval_update);
        } else {
            $this.find(`#${bare_id}`).val(new_val);
        }
        var buttons = $this.find(`#${bare_id}-buttons`);
        $(buttons.find(`[value="${new_val}"]`)).click();
        
        locks[id_num] = false;
    }
    $this.find(`.sync`).change(optionsync);
    $this.find(`.options-select`).each(optionsync);
    function toggle_buttons() {
        if ($this.find(`#${BUTTON_TAG}`).is(":checked")) {
            console.log('Buttons')
            $this.find(".options-select").hide();
            $this.find(".options-buttons").show();
        } else {
            console.log('Menus')
            $this.find(".options-select").show();
            $this.find(".options-buttons").hide();
        }
    }
    $this.find(".options-buttons").hide();
    $this.find(`#${BUTTON_TAG}`).change(toggle_buttons);

    // calculate summary
    function summary() {
        // get weights
        var weights = [];
        $this.find('.weight-input').each(function() {
            var user_i = parseInt(this.id.match(/^weight-(\d+)$/)[1]);
            while (weights.length <= user_i) {
                weights.push(0);
            }
            if (!isNaN(parseFloat(this.value))) {
                weights[user_i] = parseFloat(this.value);
            } else {
                weights[user_i] = 1;
            }
        });
        // calculate availabilty
        var totals = [];
        $this.find('.availability').each(function() {
            var m = this.id.match(/^availability-(\d+)-(\d+)$/);
            var user_i = parseInt(m[1]), option_i = parseInt(m[2]);
            while (totals.length <= option_i) {
                totals.push([0, 0]);
            }
            if (weights.length > user_i) {
                if ($(this).text().includes(AVAILABLE))
                    totals[option_i][0] += weights[user_i];
                else if ($(this).text().includes(NOT_PREFERED))
                    totals[option_i][1] += weights[user_i];
            }
        });
        // find best availability
        var best_i = 0;
        for(var i=1; i<totals.length; i++) {
            if (totals[i][0] + totals[i][1] >= totals[best_i][0] + totals[best_i][1]) {
                if (totals[i][0] + totals[i][1] > totals[best_i][0] + totals[best_i][1] || totals[i][0] > totals[best_i][0]) {
                    best_i = i;
                }
            }
        }
        // set text
        $this.find('.summary').each(function() {
            var i = parseInt(this.id.match(/^summary-(\d+)$/)[1]);
            if (totals.length) {
                $(this).text(`${totals[i][0]}+\ufeff(${totals[i][1]})`);
                if (totals[i][0] === totals[best_i][0] && totals[i][1] === totals[best_i][1]) {
                    $(this).wrapInner("<strong></strong>")
                }
            } else {
                $(this).text("0+\ufeff(0)");
                $(this).wrapInner("<strong></strong>")
            }
        });
    }
    summary();
    $this.find('.weight-input').bind('input', summary);
});