$(document).ready(function () {

    var fixHelperModified = function (e, tr) {
        var $originals = tr.children();
        var $helper = tr.clone();
        $helper.children().each(function (index) {
            $(this).width($originals.eq(index).width());
        });
        return $helper;
    };

    $("#project-list tbody").sortable({
        helper: fixHelperModified,
        stop: function (event, ui) {
            renumber_table();
            save_priorities();
        }
    }).disableSelection();
});

function renumber_table() {
    $("#project-list tbody tr").each(function() {
        var count = $(this).parent().children().index($(this)) + 1;
        $(this).find('.priority').html(count);
    });
}

function save_priorities() {
    var project_ids = [];
    $("#project-list tbody tr").each(function() {
        project_ids.push($(this).find('.id').text());
    });
    $.ajax({
        method: "POST",
        url: "/ajax/admin/projects/priority",
        data: {"project_ids": project_ids},
        error: function(data) {
            Materialize.toast(data.responseJSON.message, 4000, "red lighten-2");
        },
        traditional: true
    });
}
