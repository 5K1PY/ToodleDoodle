$(function() {
    var $this = $(this);
    function select_enabler() {
        var time1 = $this.find(`#${this.id.replace('mode', 'time1')}`);
        var time2 = $this.find(`#${this.id.replace('mode', 'time2')}`);
        if (this.value == 'Whole day') {
            time1.attr('disabled', true);
            time2.attr('disabled', true);
        } else if (this.value == 'Hourly range') {
            time1.attr('disabled', false);
            time2.attr('disabled', false);
        } else if (this.value == 'Concrete time') {
            time1.attr('disabled', false);
            time2.attr('disabled', true);
        }
    };

    function remove_row_enabler() {
        if ($this.find('.options-entry').length > 1) {
            $this.find('#remove-row').prop('disabled', false);
        } else {
            $this.find('#remove-row').prop('disabled', true);
        }
    }
    
    // Add row
    $this.find('#add-row').click(function() {
        var target = $($(this).data('target'))
        var oldrow = target.find('.options-entry:last');
        var row = oldrow.clone(true, true);
        var elem_id = row[0].id;
        var elem_num = parseInt(elem_id.replace(/options-(\d{1,4})/m, '$1')) + 1;
        row.attr('id', `options-${elem_num}`)
        row.find('input, select').each(function() {
            var id = $(this).attr('id').replace('-' + (elem_num - 1), '-' + (elem_num));
            // do not clear values
            $(this).attr('name', id).attr('id', id); // .val('').removeAttr('checked');
        });
        oldrow.after(row);
        remove_row_enabler();
    });

    // Remove row
    $this.find('#remove-row').click(function() {
        if ($this.find('.options-entry').length > 1) {
            var target = $($(this).data('target'))
            var lastRow = target.find('.options-entry:last');
            lastRow.remove();
        }
        remove_row_enabler();
    });

    $this.find('.mode').each(select_enabler).on('change', select_enabler);
    remove_row_enabler();
});
