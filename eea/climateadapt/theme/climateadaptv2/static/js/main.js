$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){q.find(".slick-prev").css("left",function(){return a()+"px"}),q.find(".slick-next").css("left",function(){return a()+45+"px"}),r.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(a){window.matchMedia("(max-width: 480px)").matches&&$.each($(".content-container table"),function(a,b){"DIV"!==$(b).parent().prop("tagName")?$(b).wrapAll('<div style="overflow-x: auto;width: 86vw; "></div>'):$(b).parent().css({"overflow-x":"auto",width:"86vw"})})}function e(){$.each($("#content .cover-richtext-tile.tile-content:not(aceitem-urban-menu-tile) ul > li"),function(a,b){var c=$(b),d=c.parent(),e=d.attr("class");void 0===e||e.indexOf("menu-urban-sub")||e.indexOf("menu-urban")||e.indexOf("aceitem-search-tile-listing")||0!==d.find("ul").length||!(c.find("a").length>0)||c.hasClass("fa")||c.addClass("fa fa-angle-double-right")})}function f(){$(".subsection-tools-general.subsection-tools-general-index_html ul li").removeClass("fa").removeClass("fa-angle-double-right"),$(".subsection-adaptation-information-climate-services.subsection-adaptation-information-climate-services-climate-services .tile-content ul li.fa.fa-angle-double-right").removeClass("fa").removeClass("fa-angle-double-right"),($(".subsection-adaptation-information-adaptation-measures-index_html .aceitem-search-tile").length>0||$(".subsection-adaptation-information-climate-services.subsection-adaptation-information-climate-services-climate-services .aceitem-search-tile").length>0)&&n(),$(".subsection-adaptation-information-adaptation-measures-index_html").length>0&&$.each($(".aceitem-search-tile li ul li"),function(a,b){var c=$(b).find("a").prop("outerHTML");$(b).replaceWith('<li class="fa fa-angle-double-right">'+c+"</li>")})}function g(){if(U){var a=$("#content-core .column.col-md-9 > div");$("#content-core .column.col-md-9").prepend('<div class="content-column"></div>'),$("#content-core .column.col-md-9 .content-column").append(a),$(" #content-core .content-column").append($(".subsection-cities-index_html #document-action-download_pdf")),$("#document-action-download_pdf").css({display:"block",clear:"both","float":"none"}),$("#document-action-download_pdf").wrap("<ul></ul>");var b=$("#content-core .column.col-md-9 .tile-default").siblings();$("#content-core div.column.col-md-9 .content-column").append('<div class="row"></div>'),$("#content-core div.column.col-md-9 .content-column > .row").append(b)}}function h(){$(".subsection-adaptation-information-observations-and-scenarios-index_html .aceitem-search-tile").length>0&&n()}function i(){$(".subsection-adaptation-information-vulnerabilities-and-risks-index_html .aceitem-search-tile").length>0&&n()}function j(){$(".subsection-adaptation-information-research-projects-index_html").length>0&&$.each($(".cover-richtext-tile.tile-content ul li"),function(a,b){$(b).find("a").length>0&&$(b).addClass("fa").addClass("fa-angle-double-right")})}function k(){$(".subsection-tools-uncertainty-guidance-index_html").length>0&&$.each($(".cover-richtext-tile.tile-content ul li"),function(a,b){$(b).find("a").length>0&&$(b).addClass("fa").addClass("fa-angle-double-right")})}function l(){$(".subsection-share-your-info-index_html").length>0&&$.each($(".cover-richtext-tile.tile-content ul li"),function(a,b){$(b).find("a").length>0&&$(b).addClass("fa").addClass("fa-angle-double-right")})}function m(){var a=[".subsection-cities.subsection-cities-index_html .aceitem-search-tile",".subsection-adaptation-information-vulnerabilities-and-risks-index_html .aceitem-search-tile",".subsection-adaptation-information-adaptation-measures-index_html .aceitem-search-tile",".subsection-adaptation-information-observations-and-scenarios-index_html .aceitem-search-tile"];$.each(a,function(a,b){$(b).parent().parent().prepend('<div class="content-sidebar"></div>');var c=$(b).parent().parent().find(".content-sidebar").siblings();$(b).parent().parent().find(".content-sidebar").append(c)})}function n(){$("#content").css({"background-color":"transparent",padding:0,margin:0,border:0}),$($("#content-core .column")[0]).prepend('<div class="content-column"></div>'),$("#content-core .content-column").append($("#content-core .content-column").siblings()),$("#content-core .content-column").append('<div class="clearfix"></div>'),$("#content-core .content-column").append($(" #document-action-download_pdf"))}function o(){$.each($(".content-column"),function(a,b){$(b).find(".tile").length>1&&$(b).find(".tile-default").css({"padding-bottom":"2rem","border-bottom":"1px solid #eee","margin-bottom":"2.5rem"})})}function p(){e(),f(),j(),g(),i(),k(),h(),l(),m(),o()}$(".slider").slick&&$(".slider").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var q=$(".slider"),r=$(".slider-caption");q.find(".slick-prev").css("left",function(){return a()+"px"}),q.find(".slick-next").css("left",function(){return a()+45+"px"}),r.css("right",function(){return a()+"px"});var s;$(window).resize(function(){clearTimeout(s),s=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-tab-heading .main-nav-tabs")}),$(".action-btn").each(function(){var a=$(this);a.hover(function(){a.hasClass("regional-btn")&&a.siblings(".action-bubble").toggleClass("regional-bubble"),a.hasClass("transnational-btn")&&a.siblings(".action-bubble").toggleClass("transnational-bubble"),a.hasClass("national-btn")&&a.siblings(".action-bubble").toggleClass("national-bubble")})}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #F2C94C",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#B8D42F",border:"2px solid #A5BF26",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".close-tab-pane").click(function(){var a=$(this).closest(".policies-tab-content"),b=$(this).closest(".sub-tab-section");b.find(".action-flex-item").removeClass("active"),a.removeClass("active")}),$(".mobile-menu i").click(function(){return $("body").toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".angle-down-icon").click(function(){$(this).parent().siblings(".sub-menu-wrapper").toggle()}),$("#user-name").click(function(a){a.preventDefault()});var t=$(".main-nav").width();$(".main-nav li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;t-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})});var u=$(".main-nav-item");u.each(function(){var a=$(this);a.find(".sub-sub-menu-wrapper").length>0&&a.find(".sub-menu-wrapper").css("column-count","2")}),$(".share-your-info-ace-button button").addClass("standard-button primary-button"),$("#document-action-download_pdf").find("a").addClass("standard-button secondary-button"),$("#login-form .formControls input").addClass("standard-button secondary-button");var v,w=window.location.pathname,x=w.split("/");v=0===x[x.length-1].length?x[x.length-2]:x[x.length-1];var y="subsection-sector-policies-"+v,z="subsection-transnational-regions-"+v,A="subsection-countries-"+v,B=$("body"),C=B.attr("class").split(/\s+/);$.each(C,function(a,b){b===y&&B.addClass("eu-policy-page"),b===z&&B.addClass("region-page"),b===A&&B.addClass("country-page")});var D=$(".eu-policy-page").length>0,E=$(".region-page").length>0,F=$(".country-page").length>0;if(D||E){var G=$(".region-page");G.find(".column.col-md-2").removeClass("col-md-2").addClass("col-md-3"),G.find(".column.col-md-10").removeClass("col-md-10").addClass("col-md-9"),G.find("#content-core .row").prepend($(".column.col-md-9")),$(".column.col-md-9").children().wrapAll('<div class="content-column"/>'),$(".column.col-md-3").children().wrapAll('<div class="content-sidebar"/>');var H=$(".content-column");H.find("img").closest(".tile-content").addClass("main-tile-content"),H.children(".col-md-4").wrapAll('<div class="row"/>'),$("#document-action-download_pdf").parent().appendTo(".content-column"),H.prepend($("#viewlet-below-content-title"))}$(".region-page #trans-region-select").siblings("div").addClass("region-countries");var I=$(".region-countries").children("strong");if(I.each(function(){$(this).replaceWith($("<h5>"+this.innerHTML+"</h5>"))}),D){var J=$(".read_more_second").children("h2");J.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))}),$(".main-tile-content").prepend('<div class="flex-wrapper"/>'),$(".flex-wrapper").append([$(".main-tile-content img"),$(".read_more_first")]);var K=$(".main-tile-content").children("h2");$(".main-tile-content").prepend([K,$(".main-tile-content").children().find("h2")]);var L=$(".content-sidebar .image-inline").parent(),M=$(".main-tile-content h2").text();L.html(function(a,b){return b.replace(/&nbsp;/g,"")}),$(".column.col-md-3").prepend(L),$(".column.col-md-3 .image-inline").parent().append('<div class="factsheet-pdf"><i class="fa fa-angle-double-right"></i><div class="factsheet-title">Factsheet on <span>'+M+"</span></div></div>"),$(".column.col-md-3 .image-inline").hide()}var N=$(".subsection-transnational-regions-baltic-sea-region-adaptation").length>0,O=$(".subsection-transnational-regions-carpathian-mountains").length>0;if((N||O)&&($("body").addClass("region-subpage"),$("#content-core .column.col-md-3").remove(),$("#content-core .column.col-md-9").removeClass("col-md-9"),$(".tile-content").addClass("clearfix"),$(function(){var a=window.location.pathname;a=a.substring(a.lastIndexOf("/")+1,a.length),$(".cover-section_nav-tile a").each(function(){var b=$(this).attr("href");b=b.substring(b.lastIndexOf("/")+1,b.length),b.indexOf(a)!==-1&&$(this).addClass("active-nav")})})),F){$(".column.col-md-10").parents(".row").removeClass("row").addClass("country-wrapper"),$(".column.col-md-2").removeClass("col-md-2"),$(".column.col-md-10").removeClass("col-md-10"),$(".sweet-tabs").attr("id","country-tab"),$(".country-wrapper .column:first-child").addClass("country-header-map"),$(".country-wrapper .column:nth-child(2)").addClass("country-content"),$(".country-select-tile").parent().addClass("countries-dropdown"),$(".country-select-tile img").remove(),$(".country-header-map").append($('<div class="country-map">')),$(".country-content .last-update-tile").addClass("clearfix").prependTo(".tab-pane"),$("table").addClass("listing"),$("#document-action-download_pdf").parent().appendTo(".tab-pane");var P=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){P.find(".selected").html($(this).text()),P.find(".selected-inp").val($(this).data("value")).trigger("change"),P.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){P.find(".options").fadeToggle().toggleClass("show"),P.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}var Q=$(".subsection-tools-adaptation-support-tool").length>0;if($(".lfc-single-image").remove(),Q){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var R=$(".tile-content").children("h1");R.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)})}var S=$(".ast-map .ast-circle");S.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var T=$(".ast-title-step").text();0==T&&$(".ast-title-step").remove(),S.each(function(){$(this).text()===T&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F"})}),$(".GlossaryHeader").parents(":eq(2)").addClass("glossary-table");var U=$(".subsection-cities.subsection-cities-index_html").length>0;d(),$(window).resize(d),p()});