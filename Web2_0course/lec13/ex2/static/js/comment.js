$('getCommentBtn').observe('click', getComment);

// send an AJAX request to server for comments
function getComment(event) {
    new Ajax.Request('/ajax/getComment', {
        method:'get',
        onSuccess: function(transport) {
            var comments = transport.responseJSON;  // convert JSON to objects

            // display each comment objects
            comments.each(function(c) {
                var div = new Element('div', {class: 'comment'})
                div.insert({bottom: new Element('span', {class: 'name'}).update(c.name)});
                div.insert({bottom: new Element('span', {class: 'time'}).update(c.time)});
                div.insert({bottom: new Element('p', {}).update(c.content)});
                $('commentsList').insert({bottom: div});
            });
        }
    });
}