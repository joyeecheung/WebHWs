$( document ).ready(function() {
    $('#tip').hide();
});

function insertTweet(time, content) {
    var $div = $("<div/>", {class: "tweet"});
    $("<p/>", {text: content}).appendTo($div);
    $("<span/>", {class: "time", text: time}).appendTo($div);
    $("#tweetList").append($div);
}

$("#submitTweet").click(function(event) {
    event.preventDefault();
    var tweet = {
        time: $.datepicker.formatDate('M. dd, yy', new Date()),
        content: $('#tweet-content').val()
    };

    $.ajax({
            url: '/ajax/addTweet',
            datatype: "json",
            type: "POST",
            data: JSON.stringify(tweet),
            contentType: "application/json charset=utf-8",
            processData: false,
            success: function (data) {
                insertTweet(tweet.time, tweet.content);
                $('#tweet-content').val('');
            },
            error: function(e){
                alert(e);
            }
    });
});

$('#avatar').mouseover(function(e){
    $('#tip').show();
});

$('#avatar').mousemove(function(e){
    var offset = $('#avatar').offset(); 
    var x = e.pageX - offset.left + 10;
    var y = e.pageY - offset.top + 10;
    $('#tip').css({"left": x + "px", top: y + "px"});
});

$('#avatar').mouseout(function(e){
    $('#tip').hide();
});
