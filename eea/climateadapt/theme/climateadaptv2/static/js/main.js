$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){h.find(".slick-prev").css("left",function(){return a()+"px"}),h.find(".slick-next").css("left",function(){return a()+45+"px"}),i.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){if(y){var a=$(".read_more_second").children("h2");a.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var b=$(".column.col-md-3");b.before(b.find(".factsheet-pdf").parent())}}function e(){if(z){$(".country-select-tile").closest(".row").css("margin","0"),$(".sweet-tabs").attr("id","country-tab");var a=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){a.find(".selected").html($(this).text()),a.find(".selected-inp").val($(this).data("value")).trigger("change"),a.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(b){a.find(".options").fadeToggle().toggleClass("show"),a.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),b.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}}function f(){if(A){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F"})})}var g=$("body");$(".slider").slick&&$(".slider").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var h=$(".slider"),i=$(".slider-caption");h.find(".slick-prev").css("left",function(){return a()+"px"}),h.find(".slick-next").css("left",function(){return a()+45+"px"}),i.css("right",function(){return a()+"px"});var j;$(window).resize(function(){clearTimeout(j),j=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-tab-heading .main-nav-tabs")}),$(".action-btn").each(function(){var a=$(this);a.hover(function(){a.hasClass("regional-btn")&&a.siblings(".action-bubble").toggleClass("regional-bubble"),a.hasClass("transnational-btn")&&a.siblings(".action-bubble").toggleClass("transnational-bubble"),a.hasClass("national-btn")&&a.siblings(".action-bubble").toggleClass("national-bubble")})}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #F2C94C",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#B8D42F",border:"2px solid #A5BF26",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".close-tab-pane").click(function(){var a=$(this).closest(".policies-tab-content"),b=$(this).closest(".sub-tab-section");b.find(".action-flex-item").removeClass("active"),a.removeClass("active")});var k=$(window).width(),l=$(".main-box"),m=0;l.each(function(){m=$(this).outerHeight()>m?$(this).outerHeight():m}),k<=600?l.css("min-height","auto"):l.css("min-height",m),$(".mobile-menu i").click(function(){return g.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".toggle-down").click(function(){return $(this).parent().siblings(".sub-menu-wrapper").toggle(),$(this).parent().parent().siblings().children(".sub-menu-wrapper").hide(),!1}),$("#user-name").click(function(a){a.preventDefault()});var n=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;n-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})}),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button"),$(".CSSTableGenerator").addClass("listing");var o=$(".bluebutton");o.addClass("standard-button primary-button"),o.parent().css("text-align","left");var p=$("input[type=submit]");p.each(function(){"Save"===$(this).val()?$(this).addClass("standard-button primary-button"):"Cancel"===$(this).val()?$(this).addClass("standard-button secondary-button"):$(this).addClass("standard-button secondary-button")});var q=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(q.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(q)>-1)&&a.addClass("active-nav")});var r,s=window.location.pathname,t=s.split("/");r=0===t[t.length-1].length?t[t.length-2]:t[t.length-1],r="index_html"===r?t[t.length-3]:t[t.length-1];var u="subsection-sector-policies-"+r,v="subsection-transnational-regions-"+r,w="subsection-countries-"+r,x=void 0!==g.attr("class")?g.attr("class").split(/\s+/):[];$.each(x,function(a,b){b===u&&g.addClass("eu-policy-page"),b===v&&g.addClass("region-page"),b===w&&g.addClass("country-page")});var y=$(".eu-policy-page").length>0,z=$(".country-page").length>0,A=($(".subsection-transnational-regions-baltic-sea-region-adaptation").length>0,$(".subsection-transnational-regions-carpathian-mountains").length>0,$(".subsection-tools-adaptation-support-tool").length>0),B=$(".subsection-transnational-regions .column.col-md-3");B.after(B.find(".detailed-content").parentsUntil(".tile-default")),d(),e(),f(),$(".region-page #trans-region-select").siblings("div").addClass("region-countries");var C=$(".region-countries").children("strong");C.each(function(){$(this).replaceWith($("<h5>"+this.innerHTML+"</h5>"))}),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),$('#search-field input[type="text"]').attr("placeholder","type here...");var D=$(".subsection-tools-urban-ast h2");D.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var E=$(".subsection-tools-urban-ast").length>0;E&&$(".cover-richtext-tile ul li a").attr("target","_blank");var F=$("#document-action-download_pdf");if(s.indexOf("/tools/urban-ast")!==-1&&s.indexOf("pdf.body")===-1){var G='<a href="/tools/urban-ast/download.pdf"class="standard-button ast-section-pdf">Download section as PDF</a>';F.parent().before(G)}if(s.indexOf("/tools/adaptation-support-tool")!==-1&&s.indexOf("pdf.body")===-1){var G='<a href="/tools/adaptation-support-tool/download.pdf"class="standard-button ast-section-pdf">Download section as PDF</a>';F.parent().before(G)}$(".tile-container").each(function(){var a=$(this),b=a.find(".tile-type-name"),c=a.children("a"),d=a.children("div");"Relevant AceContent"==b.text()&&b.detach().appendTo(d),"Edit"==c.text()&&c.detach().appendTo(d)});var H=$(".panel-title a");H.click(function(){var a=$(this),b=a.text().toLowerCase();(b.indexOf("read more")>-1||b.indexOf("read less")>-1)&&a.text(function(a,b){return"Read more"==b?"Read less":"Read more"})}),window.location.href.indexOf("data-and-downloads")>-1&&F.parent().hide();var I=$(".speedbutton");if(I.length>0){var B=$(".col-md-3.content-sidebar"),J=I.closest(".tile-default"),K=J.prev();K.addClass("interactive-maps"),B.after(B.find(K)),K.append(J)}var L=$("#links");L.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var b=L.children(".gallery-hide").length;L.children(".gallery-hide").slice(1,b).css("display","none")}}),$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}}),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var M=$(".subsection-case-studies .aceitem_page .col-md-3");M.before(M.find(".case-studies-illustrations")),M.before(M.find(".sidebar_files"));var N=$(".use-cases-listing tbody tr");N.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")}),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var O=$(".subsection-tools-urban-adaptation-climatic-threats").length>0;O&&g.addClass("fullwidth")});