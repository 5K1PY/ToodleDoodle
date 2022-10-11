$(function() {
    var $this = $(this);
    var options = [];
    for (var i=0;; i++) {
        var option = $this.find(`#options-${i}`);
        if (option.val() === undefined) {
            break;
        }
        options.push(option.val());
    }
    console.log(options);

    $this.find('.option-select').on('change', function() {
        var i = parseInt($(this).attr('id').match(/^options-(\d)/)[1]);
        if ($this.find('#interval-mode').is(":checked")) {
            console.log(options);
            for (var j=i+1; j < options.length && options[i] === options[j]; j++) {
                console.log(j);
                $this.find(`#options-${j}`).val(this.value).change();
            }
        }
        options[i] = this.value;
    });
});
