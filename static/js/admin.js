function confirm_deletion(element) {
    $('#confirm-dialog').openModal();
    $('#confirm-dialog-yes').click(function() {
        $('#confirm-dialog').closeModal();
        document.location = element.href;
    });
}

function generate_markdown_preview(converter, markdown_div, result_div) {
    var text = markdown_div.val();
    var markdown = converter.makeHtml(text);
    result_div.html(markdown);
}

function set_tag_ids(tags_div, tag_ids) {
    tags_div.val(JSON.stringify(tag_ids));
}
