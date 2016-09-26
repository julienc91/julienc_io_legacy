$(document).ready(function(){

    var tag_ids = [];
    var converter = new showdown.Converter();
    $("#content").on("input paste keyup", function() {
        generate_markdown_preview(converter, $("#content"), $("#content-preview"));
    });
    generate_markdown_preview(converter, $("#content"), $("#content-preview"));

    $('#tags .chip.enabled').each(function(_, chip) {
        var tag_id = $(chip).data("tag-id");
        tag_ids.push(tag_id);
    });

    $('.chip').click(function(e) {
        var tag_id = $(this).data("tag-id");
        if ($(this).hasClass("enabled")) {
            $(this).addClass("disabled");
            $(this).removeClass("enabled");
            var index = tag_ids.indexOf(tag_id);
            if (index >= 0)
                tag_ids.splice(index, 1);
        } else {
            $(this).addClass("enabled");
            $(this).removeClass("disabled");
            tag_ids.push(tag_id);
        }
        set_tag_ids($("#tag-ids"), tag_ids);
    });
    set_tag_ids($("#tag-ids"), tag_ids);
});
