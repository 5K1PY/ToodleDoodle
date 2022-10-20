$(function() {
    var $this = $(this);

    // constants
    var AVAILABLE = "✅";
    var NOT_PREFERED = "(✔️)";
    var MODES = {
        't': 'transpose-tables',
        'i': 'interval-mode',
        'w': 'weights',
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
    $this.find('.option-select').change(function() {
        var i = parseInt($(this).attr('id').match(/^options-(\d+)$/)[1]);
        if ($this.find('#interval-mode').is(":checked")) {
            for (var j=i+1; j < options.length && options[i] === options[j]; j++) {
                $this.find(`#options-${j}`).val(this.value).change();
            }
        }
        options[i] = this.value;
    });

    // transpose table
    $this.find('#transpose-tables').change(function() {
        console.log("TODO: transpose tables");
    });

    // show / hide weights
    function toggle_weights() {
        if ($(this).is(":checked")) {
            $this.find(".edit-button").hide();
            $this.find(".delete-button").hide();
            $this.find(".weight").show();
        } else {
            $this.find(".edit-button").show();
            $this.find(".delete-button").show();
            $this.find(".weight").hide();
        }
    }
    $this.find('#weights').each(toggle_weights).change(toggle_weights);

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
                $(this).text(`${totals[i][0]}+(${totals[i][1]})`);
                if (totals[i][0] === totals[best_i][0] && totals[i][1] === totals[best_i][1]) {
                    $(this).wrapInner("<strong></strong>")
                }
            } else {
                $(this).text("0+(0)");
                $(this).wrapInner("<strong></strong>")
            }
        });
    }
    summary();
    $this.find('.weight-input').bind('input', summary);

    // enable tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // add shortcuts
    $this.keypress(function(e) {
        var key = String.fromCharCode(e.keyCode || e.which);
        console.log(key);
        if (key == 's') {
            $this.find('#show-settings').click();
        }
        for (const bound_key in MODES) {
            if (key == bound_key) {
                $this.find(`#${MODES[bound_key]}`).click();
            }
        }
    });
});
