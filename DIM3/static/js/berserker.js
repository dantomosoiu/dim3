var tabCounter = 0;
var roomName = "";

$(document).ready(function () {

    //tabCounter = 3;

    //setTabSelectorClick();

    //checkRoomRequest();

    var Tabs = {
	        'Categories'   : 'BerserkerChat/Categories',
	        'Recent'   : 'BerserkerChat/Recent',
	        'Chat' : 'BerserkerChat/room/room'
	    }
    var colors = ['blue']
    /* The colors of the line above the tab when it is active: */

    var topLineColor = {
        blue:'lightblue'
    }

    /* Looping through the Tabs object: */
    var z=0;
    $.each(Tabs,function(i,j){
        /* Sequentially creating the tabs and assigning a color from the array: */

        var tmp = $('<li><a href="#" class="tab btn btn-inverse">'+i+' <span class="left" /><span class="right" /></a></li>');

        /* Setting the page data for each hyperlink: */

        tmp.find('a').data('page',j);

        /* Adding the tab to the UL container: */
        $('ul.tabContainer').append(tmp);
    })

    var the_tabs = $('.tab');

    the_tabs.click(function(e){
        /* "this" points to the clicked tab hyperlink: */
        var element = $(this);

        href= "http://".concat(getHostname().hostname.concat(element.data('page')));

        /* If it is currently active, return false and exit: */
        if(element.find('#overLine').length) return false;
        if(element.is(the_tabs.eq(0))) {
            $("#category-filter").show();
        }else {
            $("#category-filter").hide();
        }
        if(element.is(the_tabs.eq(2))) {
            if( $("#left-pane").attr("data-name") == "" ) {
                name = prompt("Please Enter a Screen Name");
                if(name == "") {
                    name = "Anonymous";
                }

                Dajaxice.BerserkerChat.createGuestName(updateUser, {'name' : name});
            }
            href = "http://".concat(getHostname().hostname.concat(getHostname().roomname));
        }

        /* Detecting the color of the tab (it was added to the class attribute in the loop above): */
        var bg = element.attr('class').replace('tab ','');

        /* Removing the line: */
        $('#overLine').remove();

        /* Creating a new line with jQuery 1.4 by passing a second parameter: */
        $('<div>',{
            id:'overLine',
            css:{
                display:'none',
                width:element.outerWidth()-2,
                background:topLineColor[bg] || 'white'
            }}).appendTo(element).fadeIn('slow');

        /* Checking whether the AJAX fetched page has been cached: */

        if(!element.data('cache'))
        {
            /* If no cache is present, show the gif preloader and run an AJAX request: */
            var loadImgLoc = "<img src=".concat("http://".concat(getHostname().hostname).concat("static/img/ajax_preloader.gif")).concat(" width=\"64\" height=\"64\" class=\"preloader\" />");
            $('#contentHolder').html('<img src="static/img/ajax_preloader.gif" width="64" height="64" class="preloader" />');

            $.get(href,function(msg){

                $('#contentHolder').html(msg);


            });
        }
        else $('#contentHolder').html(element.data('cache'));

        roomName = getHostname().roomname;



        e.preventDefault();
    })

    /* Emulating a click on the first tab so that the content area is not empty: */
    the_tabs.eq(0).click();


    $('#category-filter').change(function() {
        $('.main-category').next('ul').removeClass("list-inactive");
        $('.main-category').next('ul').addClass("list-active");
        $('.room-list-element').css("display", "");
        var val = $('#category-filter').val();
        if(val != ''){
            val = val.toLowerCase();
            console.log(val);
            $('.room-list-element').css("display", "none");
            $('.room-list-element').each(function( index ) {
                var cat = $($(this).children()[0]).text();
                if(cat == null || cat == undefined || cat == ""){

                } else {
                    if(cat.toLowerCase().indexOf(val) > -1){
                        $(this).css("display", "");
                    }
                }
            });
        }
    });

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

function refreshMe(data){
    window.location = "http://".concat(getHostname().hostname.concat("room/").concat(data.name))
}

function updateUser(data){
    $("#left-pane").attr("data-name",data);
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

function createPrivateChat(){
    Dajaxice.BerserkerChat.getPrivateRoom(refreshMe);
}


function createPublicChat(){
    var roomName=document.forms["new-public-form"]["create-public-chat-subject"].value.replace(/ /g,"_").toLowerCase().replace(/[^\w\s]|/g, "").substring(0,60);
    Dajaxice.BerserkerChat.getPublicRoom(refreshMe, {'roomname': roomName});
}


var csrftoken = getCookie('csrftoken');