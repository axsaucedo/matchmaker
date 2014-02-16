var home = {
    init : function() {
        function parallax(){
            var scrolled = $(window).scrollTop();

            $("#main-title").css("margin-left", 40+(scrolled*3));
            $("#content").css("background-position", "0px " + scrolled + "px");
            console.log("0px " + scrolled + "px");
        }

        $(window).scroll(function(e){
            parallax();
        });
    }
}

$(function() {
    home.init();
});