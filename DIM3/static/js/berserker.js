var tabCounter = 0;

$(document).ready(function () {

    tabCounter = 3;

    setTabSelectorClick();


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
    addTab("it worked!", data.tabContent);
}
