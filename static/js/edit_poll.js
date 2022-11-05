$(function() {
    var $this = $(this);

    // Add row
    $this.find('#add-row').click(function() {
        var target = $($(this).data('target'))
        var old_entry = target.find('.options-entry:last');
        var new_entry = old_entry.clone(true, true);
        var elem_id = $(new_entry).attr('id');
        var elem_num = parseInt(elem_id.replace(/options-(\d{1,4})/m, '$1')) + 1;
        new_entry.attr('id', `options-${elem_num}`);
    
        // Rename ids and names
        new_entry.find('input, div, button').each(function() {
            console.log(this);
            if ($(this).attr('id')) {
                var id = $(this).attr('id').replace('-' + (elem_num - 1), '-' + (elem_num));
                $(this).attr('name', id).attr('id', id)
            }
            if ($(this).attr('placeholder')) {
                var placeholder = $(this).attr('placeholder').replace(elem_num - 1, elem_num);
                $(this).attr('placeholder', placeholder)
            }
            if ($(this).attr('data-target')) {
                var data_target = $(this).attr('data-target').replace('-' + (elem_num - 1), '-' + (elem_num));
                $(this).attr('data-target', data_target)
            }
            if (this.tagName != "DIV") {
                var class_ = $(this).attr('class').replace('-' + (elem_num - 1), '-' + (elem_num));
                $(this).attr('class', class_);
            }
        });

        // Clear values
        new_entry.find('input').each(function() {
            $(this).val('');
        });

        new_entry.find()
        old_entry.after(new_entry);
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
})