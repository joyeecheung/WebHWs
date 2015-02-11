function insertComment(name, time, content) {
    var $div = $("<div/>", {class: "comment"});
    $("<span/>", {class: "name", text: name}).appendTo($div);
    $("<span/>", {class: "time", text: time}).appendTo($div);
    $("<p/>", {text: content}).appendTo($div);
    $div.appendTo($("#commentsList"));
}

$("#getCommentBtn").click(function() {
    $.getJSON("/ajax/getComment", function(comments) {
        $.each(comments, function(i, c) {
            insertComment(c.name, c.time, c.content);
        });
    });
});

$("#submit").click(function() {
    event.preventDefault();
    var cd = {
        name: $('#comment-name').text(),
        time: $.datepicker.formatDate('M. dd, yy', new Date()),
        content: $('#comment-content').val()
    };

    $.ajax({
            url: '/ajax/addComment',
            datatype: "json",
            type: "POST",
            data: JSON.stringify(cd),
            contentType: "application/json charset=utf-8",
            processData: false,
            success: function (data) {
                insertComment(cd.name, cd.time, cd.content)
            },
            error: function(e){
                alert(e);
            }
    });
});

