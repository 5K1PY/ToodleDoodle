$(function() {
    var $this = $(this);
    function select_day_enabler() {
        var day1 = $this.find(`#${this.id.replace('day_mode', 'day1-box')}`);
        var from = $this.find(`#${this.id.replace('day_mode', 'day_from')}`);
        var day2 = $this.find(`.${this.id.replace('day_mode', 'day2-box-inside')}`);
        var increment = $this.find(`.${this.id.replace('day_mode', 'day_increment-box-inside')}`);
        if (this.value == 'One day') {
            day1.removeClass("input-group");
            from.attr('hidden', true);
            day2.hide();
            increment.hide();
        } else if (this.value == 'Range of days') {
            day1.addClass("input-group");
            from.attr('hidden', false);
            day2.show();
            increment.show();
        }
    };

    function select_time_enabler() {
        var time1_box = $this.find(`#${this.id.replace('time_mode', 'time1-box')}`);
        var time2_box = $this.find(`#${this.id.replace('time_mode', 'time2-box')}`);

        var time1 = $this.find(`#${this.id.replace('time_mode', 'time1')}`);
        var time2 = $this.find(`#${this.id.replace('time_mode', 'time2')}`);
        var time3 = $this.find(`#${this.id.replace('time_mode', 'time3-box')}`);
        var from = $this.find(`#${this.id.replace('time_mode', 'time_from')}`);
        var to = $this.find(`#${this.id.replace('time_mode', 'time_to')}`);
        var time_increment = $this.find(`#${this.id.replace('time_mode', 'time_increment-box')}`);
        if (this.value == 'Whole day') {
            time1.attr('hidden', true);
            time2.attr('hidden', true);
            time3.attr('hidden', true);
            from.attr('hidden', true);
            to.attr('hidden', true);
            time_increment.attr('hidden', true);
        } else if (this.value == 'Hourly range') {
            time1_box.addClass("input-group");
            time2_box.addClass("input-group");
            time1.attr('hidden', false);
            time2.attr('hidden', false);
            time3.attr('hidden', true);
            time_increment.attr('hidden', false);
            from.attr('hidden', false);
            to.attr('hidden', false);
        } else if (this.value == 'Various times') {
            time1_box.removeClass("input-group");
            time2_box.removeClass("input-group");
            time1.attr('hidden', false);
            time2.attr('hidden', false);
            time3.attr('hidden', false);
            time_increment.attr('hidden', true);
            from.attr('hidden', true);
            to.attr('hidden', true);
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
        var old_entry = target.find('.options-entry:last');
        console.log(old_entry)
        var new_entry = old_entry.clone(true, true);
        var elem_id = new_entry[0].id;
        var elem_num = parseInt(elem_id.replace(/options-(\d{1,4})/m, '$1')) + 1;
        new_entry.attr('id', `options-${elem_num}`);
        new_entry.find('input, select, span, div').each(function() {
            var id = $(this).attr('id').replace('-' + (elem_num - 1), '-' + (elem_num));
            var class_ = $(this).attr('class').replace('-' + (elem_num - 1), '-' + (elem_num));
            $(this).attr('name', id).attr('id', id).attr('class', class_);
        });
        new_entry.find('input').each(function() {
            $(this).val('');
        });
        old_entry.after(new_entry);
        $this.find('.time-mode').each(select_time_enabler);
        $this.find('.day-mode').each(select_day_enabler);
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

    $this.find('.time-mode').each(select_time_enabler).on('change', select_time_enabler);
    $this.find('.day-mode').each(select_day_enabler).on('change', select_day_enabler);
    remove_row_enabler();
});
