$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){j.find(".slick-prev").css("left",function(){return a()+"px"}),j.find(".slick-next").css("left",function(){return a()+45+"px"}),k.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){if(x){var a=$(".read_more_second").children("h2");a.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var b=$(".content-sidebar .image-inline").parent(),c=$(".tile-title").text();b.html(function(a,b){return b.replace(/&nbsp;/g,"")}),$(".column.col-md-3").prepend(b),$(".column.col-md-3 .image-inline").parent().append('<div class="factsheet-pdf"><i class="fa fa-angle-double-right"></i><div class="factsheet-title">Factsheet on <span>'+c+"</span></div></div>"),$(".column.col-md-3 .image-inline").hide()}}function e(){(z||A)&&(i.addClass("region-subpage"),$("#content-core .column.col-md-3").remove(),$("#content-core .column.col-md-9").removeClass("col-md-9"),$(".tile-content").addClass("clearfix"),$(function(){var a=window.location.pathname;a=a.substring(a.lastIndexOf("/")+1,a.length),$(".cover-section_nav-tile a").each(function(){var b=$(this).attr("href");b=b.substring(b.lastIndexOf("/")+1,b.length),b.indexOf(a)!==-1&&$(this).addClass("active-nav")})}))}function f(){if(y){$("#content-core").children().addClass("country-wrapper").removeClass("row"),$(".sweet-tabs").attr("id","country-tab");var a=$(".country-select-tile");a.parent().addClass("countries-dropdown"),a.find("img").remove();var b=$(".tab-pane");$(".country-header-map").append($('<div class="country-map">')),$(".country-content .last-update-tile").addClass("clearfix").prependTo(b),$("table").addClass("listing"),$("#document-action-download_pdf").parent().appendTo(b);var c=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){c.find(".selected").html($(this).text()),c.find(".selected-inp").val($(this).data("value")).trigger("change"),c.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){c.find(".options").fadeToggle().toggleClass("show"),c.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}}function g(){if(B){$(".lfc-single-image").remove(),$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)})}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F"})})}function h(a){window.matchMedia("(max-width: 480px)").matches&&$.each($(".content-container table"),function(a,b){"DIV"!==$(b).parent().prop("tagName")?$(b).wrapAll('<div style="overflow-x: auto;width: 86vw; "></div>'):$(b).parent().css({"overflow-x":"auto",width:"86vw"})})}var i=$("body");$(".slider").slick&&$(".slider").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var j=$(".slider"),k=$(".slider-caption");j.find(".slick-prev").css("left",function(){return a()+"px"}),j.find(".slick-next").css("left",function(){return a()+45+"px"}),k.css("right",function(){return a()+"px"});var l;$(window).resize(function(){clearTimeout(l),l=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-tab-heading .main-nav-tabs")}),$(".action-btn").each(function(){var a=$(this);a.hover(function(){a.hasClass("regional-btn")&&a.siblings(".action-bubble").toggleClass("regional-bubble"),a.hasClass("transnational-btn")&&a.siblings(".action-bubble").toggleClass("transnational-bubble"),a.hasClass("national-btn")&&a.siblings(".action-bubble").toggleClass("national-bubble")})}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #F2C94C",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#B8D42F",border:"2px solid #A5BF26",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".close-tab-pane").click(function(){var a=$(this).closest(".policies-tab-content"),b=$(this).closest(".sub-tab-section");b.find(".action-flex-item").removeClass("active"),a.removeClass("active")});var m=$(".main-box"),n=0;m.each(function(){n=$(this).outerHeight()>n?$(this).outerHeight():n}),m.css("min-height",n),$(".mobile-menu i").click(function(){return i.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".angle-down-icon").click(function(){$(this).parent().siblings(".sub-menu-wrapper").toggle()}),$("#user-name").click(function(a){a.preventDefault()});var o=$(".main-nav").width();$(".main-nav li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;o-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})});var p=$(".main-nav-item");p.each(function(){var a=$(this);a.find(".sub-sub-menu-wrapper").length>0&&a.find(".sub-menu-wrapper").css("column-count","2")}),$("#document-action-download_pdf").addClass("standard-button secondary-button"),$("#login-form .formControls input").addClass("standard-button secondary-button");var q,r=window.location.pathname,s=r.split("/");q=0===s[s.length-1].length?s[s.length-2]:s[s.length-1];var t="subsection-sector-policies-"+q,u="subsection-transnational-regions-"+q,v="subsection-countries-"+q,w=void 0!==i.attr("class")?i.attr("class").split(/\s+/):[];$.each(w,function(a,b){b===t&&i.addClass("eu-policy-page"),b===u&&i.addClass("region-page"),b===v&&i.addClass("country-page")});var x=$(".eu-policy-page").length>0,y=$(".country-page").length>0,z=$(".subsection-transnational-regions-baltic-sea-region-adaptation").length>0,A=$(".subsection-transnational-regions-carpathian-mountains").length>0,B=$(".subsection-tools-adaptation-support-tool").length>0,C=$(".content-column");C.find("h2").first().addClass("tile-title"),d(),e(),f(),g(),$(".region-page #trans-region-select").siblings("div").addClass("region-countries");var D=$(".region-countries").children("strong");D.each(function(){$(this).replaceWith($("<h5>"+this.innerHTML+"</h5>"))}),$(".GlossaryHeader").parents(":eq(2)").addClass("glossary-table"),$(".aceitem-search-tile-listing li ul li").each(function(){var a=$(this);a.html(a.html().replace("»",""))}),h(),$(window).resize(h)});