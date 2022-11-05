$(function() {
    var $this = $(this);

    function rename(el, from, to) {
        console.log(el);
        if ($(el).attr('id')) {
            var id = $(el).attr('id').replace('-' + from, '-' + to);
            $(el).attr('id', id);
        }
        if ($(el).attr('name')) {
            $(el).attr('name', id);
        }
        if ($(el).attr('placeholder')) {
            var placeholder = $(el).attr('placeholder').replace(from+1, to+1);
            $(el).attr('placeholder', placeholder)
        }
        if ($(el).attr('data-target')) {
            var data_target = $(el).attr('data-target').replace('-' + from, '-' + to);
            $(el).attr('data-target', data_target)
        }
        if ($(el).attr('class')) {
            var class_ = $(el).attr('class').replace('s-' + from, 's-' + to);
            $(el).attr('class', class_);
        }
    }

    function rename_recursive(el, from, to) {
        rename(el, from, to)
        // Rename ids and names
        $(el).find('*').each(function () {
            rename(this, from, to);
        });
    }

    function delete_enabler() {
        if ($this.find('.options-entry').length <= 1) {
            $this.find('.delete-option').prop('disabled', true);
        } else {
            $this.find('.delete-option').prop('disabled', false);
        }
    }

    // Add row
    $this.find('#add-row').click(function() {
        var target = $($(this).data('target'))
        var old_entry = target.find('.options-entry:last');
        var new_entry = old_entry.clone(true, true);
        var elem_id = $(new_entry).attr('id');
        var elem_num = parseInt(elem_id.replace('option-', ''));
        rename_recursive(new_entry, elem_num, elem_num+1);

        // Clear values
        new_entry.find('input').each(function() {
            $(this).val('');
        });

        new_entry.find()
        old_entry.after(new_entry);
        delete_enabler();
    });

    // Remove row
    $this.find('.delete-option').click(function() {
        if ($this.find('.options-entry').length <= 1) {
            return;
        }
        var rem_num = parseInt($(this).data('target').replace('#option-', ''));
        var target = $($(this).data('target'));
        target.remove();
        $this.find(".options-entry").each(function() {
            var option_num = parseInt($(this).attr('id').replace('option-', ''));
            if (option_num > rem_num) {
                rename_recursive(this, option_num, option_num-1);
            }
        });
        delete_enabler();
    });
})