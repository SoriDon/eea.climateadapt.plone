$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){i.find(".slick-prev").css("left",function(){return a()+"px"}),i.find(".slick-next").css("left",function(){return a()+45+"px"}),j.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){if(A){var a=$(".content-column");a.find("h2").first().addClass("tile-title");var b=$(".read_more_second").children("h2");b.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var c=$(".content-sidebar .image-inline").parent(),d=$(".tile-title").text();c.html(function(a,b){return b.replace(/&nbsp;/g,"")}),$(".column.col-md-3").prepend(c),$(".column.col-md-3 .image-inline").parent().append('<div class="factsheet-pdf"><i class="fa fa-angle-double-right"></i><div class="factsheet-title">Factsheet on <span>'+d+"</span></div></div>"),$(".column.col-md-3 .image-inline").hide()}}function e(){(C||D)&&(h.addClass("region-subpage"),$("#content-core .column.col-md-3").remove(),$("#content-core .column.col-md-9").removeClass("col-md-9"),$(".tile-content").addClass("clearfix"))}function f(){if(B){$("#content-core").children().addClass("country-wrapper").removeClass("row"),$(".sweet-tabs").attr("id","country-tab");var a=$(".country-select-tile");a.parent().addClass("countries-dropdown"),a.find("img").remove();var b=$(".tab-pane");$(".country-header-map").append($('<div class="country-map">')),$(".country-content .last-update-tile").addClass("clearfix").prependTo(b),$("table").addClass("listing"),$("#document-action-download_pdf").parent().appendTo(b);var c=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){c.find(".selected").html($(this).text()),c.find(".selected-inp").val($(this).data("value")).trigger("change"),c.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){c.find(".options").fadeToggle().toggleClass("show"),c.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}}function g(){if(E){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)})}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F"})})}var h=$("body");$(".slider").slick&&$(".slider").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var i=$(".slider"),j=$(".slider-caption");i.find(".slick-prev").css("left",function(){return a()+"px"}),i.find(".slick-next").css("left",function(){return a()+45+"px"}),j.css("right",function(){return a()+"px"});var k;$(window).resize(function(){clearTimeout(k),k=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-tab-heading .main-nav-tabs")}),$(".action-btn").each(function(){var a=$(this);a.hover(function(){a.hasClass("regional-btn")&&a.siblings(".action-bubble").toggleClass("regional-bubble"),a.hasClass("transnational-btn")&&a.siblings(".action-bubble").toggleClass("transnational-bubble"),a.hasClass("national-btn")&&a.siblings(".action-bubble").toggleClass("national-bubble")})}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #F2C94C",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#B8D42F",border:"2px solid #A5BF26",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".close-tab-pane").click(function(){var a=$(this).closest(".policies-tab-content"),b=$(this).closest(".sub-tab-section");b.find(".action-flex-item").removeClass("active"),a.removeClass("active")});var l=$(window).width(),m=$(".main-box"),n=0;m.each(function(){n=$(this).outerHeight()>n?$(this).outerHeight():n}),l<=600?m.css("min-height","auto"):m.css("min-height",n),$(".mobile-menu i").click(function(){return h.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".angle-down-icon").click(function(){$(this).parent().siblings(".sub-menu-wrapper").toggle()}),$("#user-name").click(function(a){a.preventDefault()});var o=$(".main-nav").width();$(".main-nav li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;o-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})});var p=$(".main-nav-item");p.each(function(){var a=$(this);a.find(".sub-sub-menu-wrapper").length>0&&a.find(".sub-menu-wrapper").css("column-count","2")}),$("#document-action-download_pdf, #login-form .formControls input, #folderlisting-main-table .context").addClass("standard-button secondary-button"),$(".CSSTableGenerator").addClass("listing");var q=$(".bluebutton");q.addClass("standard-button primary-button"),q.parent().css("text-align","left");var r=$("input[type=submit]");r.each(function(){"Save"===$(this).val()?$(this).addClass("standard-button primary-button"):"Cancel"===$(this).val()&&$(this).addClass("standard-button secondary-button")});var s=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(s.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(s)>-1)&&a.addClass("active-nav")});var t,u=window.location.pathname,v=u.split("/");t=0===v[v.length-1].length?v[v.length-2]:v[v.length-1],t="index_html"===t?v[v.length-3]:v[v.length-1];var w="subsection-sector-policies-"+t,x="subsection-transnational-regions-"+t,y="subsection-countries-"+t,z=void 0!==h.attr("class")?h.attr("class").split(/\s+/):[];$.each(z,function(a,b){b===w&&h.addClass("eu-policy-page"),b===x&&h.addClass("region-page"),b===y&&h.addClass("country-page")});var A=$(".eu-policy-page").length>0,B=$(".country-page").length>0,C=$(".subsection-transnational-regions-baltic-sea-region-adaptation").length>0,D=$(".subsection-transnational-regions-carpathian-mountains").length>0,E=$(".subsection-tools-adaptation-support-tool").length>0;d(),e(),f(),g(),$(".region-page #trans-region-select").siblings("div").addClass("region-countries");var F=$(".region-countries").children("strong");F.each(function(){$(this).replaceWith($("<h5>"+this.innerHTML+"</h5>"))}),$(".GlossaryHeader").parents(":eq(2)").addClass("glossary-table");var G=$(".glossary-table"),H=$('<ul class="glossary-list"/>');H.insertBefore(G);var I={letters:[]},J=G.find(".GlossaryHeader a");J.each(function(){var a,b=$(this).text();if(0===b.indexOf("(")){var c=b.split(")")[1],c=c.replace(/^\s+/g,"");a=c.substring(0,1).toUpperCase()}else a=$(this).text().substring(0,1).toUpperCase();a in I||(I[a]=[],I.letters.push(a)),I[a].push($(this))}),I.letters.sort(),G.remove(),$.each(I.letters,function(a,b){I[b].sort(function(a,b){return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase())});var c=$("<ul/>");$.each(I[b],function(a,b){var d=$("<li/>");c.append(d),d.append(b)}),$(".glossary-list").append($("<li/>").append($("<a/>").attr("name",b.toLowerCase()).addClass("g-heading").html(b)).append(c))}),$(".aceitem-search-tile-listing li ul li").each(function(){var a=$(this);a.html(a.html().replace("»",""))}),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),$(".news-item").parent().parent().children("h2").addClass("news-title"),$('#search-field input[type="text"]').attr("placeholder","type here...")});