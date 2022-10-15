$(function() {
    var $this = $(this);

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

    // enable tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // add shortcuts
    $this.keypress(function(e) {
        var key = String.fromCharCode(e.keyCode || e.which);
        if (key == 's') {
            $this.find('#show-settings').click();
        } else if (key == 't') {
            $this.find('#transpose-tables').click();
        } else if (key == 'i') {
            $this.find('#interval-mode').click();
        } else if (key == 'w') {
            $this.find('#weights').click();
        }
    });
});
