var tabCounter = 0;

$(document).ready(function () {

    tabCounter = 3;

    setTabSelectorClick();

    checkRoomRequest();

});



var addTab = function (name, content) {
    tabCounter++;
    $('#tab-list > div').hide();
    $('#tab-selector li').removeClass("active");
    $('#tab-selector li').addClass("inactive");
    $('#tab-selector ul').append("<li data-tab-selector='" + tabCounter + "' class=\"active\">" + name + "</li> ");
    setTabSelectorClick();

    var newTab = document.createElement("div");
    $(newTab).html(content);
    newTab.setAttribute("id", "tab-"+tabCounter);
    $("#tab-list").append(newTab);
    $(newTab).show();
};

var checkRoomRequest = function(){
    var req = $("body").attr("data-request");

    var pieces = req.split('/');

        console.log(pieces);

        if(pieces[1] == "room" && pieces[2].match("^[a-zA-Z0-9]+$")){
            createChat(pieces[2]);
        }
}

var setTabSelectorClick = function(){
    $('#tab-selector li').click(function (event) {
        $('#tab-list > div').hide();
        $('#tab-selector li').removeClass("active");
        $('#tab-selector li').addClass("inactive");
        $(event.target).removeClass("inactive");
        $(event.target).addClass("active");

        $('#tab-' + $(event.target).attr("data-tab-selector")).show();
    });
}

function my_callback(data){
    addTab(data.name, data.tab);
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createChat(roomName){
    var name = "";

    if( $("#left-pane").attr("data-name") == "" ) {
        name = prompt("Please enter an username");
    }
    console.log("fgm");

    Dajaxice.BerserkerChat.getRoom(my_callback, {'name' : name, 'room' : roomName});
}


var csrftoken = getCookie('csrftoken');