function initSlider(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){$(".slider-caption, .slider-nav").css("right",function(){return a()+"px"}),$(".image-copyright").css("left",function(){return a()+"px"})}if($(".slider").slick){$(".slider-for").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var c=$(".slider-thumb");c.click(function(a){a.preventDefault();var b=$(this).index();$(".slider-for").slick("slickGoTo",parseInt(b))}),c.mouseenter(function(){$(".slider-for").slick("slickPause")}).mouseleave(function(){$(".slider-for").slick("slickPlay")}),$(".slider-for").on("setPosition",function(){var a=$(".slider-for").slick("slickCurrentSlide")+1;c.removeClass("active-slider"),$(".slider-thumb:nth-child("+a+")").addClass("active-slider")})}return setTimeout(function(){$(".slider-caption, .slider-nav, .image-copyright").fadeIn(700)},200),$(".slider-caption, .slider-nav").css("right",function(){return a()+"px"}),$(".image-copyright").css("left",function(){return a()+"px"}),b}function initMainArea(){function a(){$(this).width()>=767?c.css("height",d):c.css("height","")}var b=$(window).width(),c=$(".main-box"),d=0;return c.each(function(){d=$(this).outerHeight()>d?$(this).outerHeight():d}),b>=767?c.css("height",d):c.css("height",""),a}function initMainTabs(){function a(a,b){for(var c=$(b),d=$(a),e=c.width(),f=d.outerWidth(!0),g=d.index(),h=0,i=c.find("li"),j=0;j<g;j++)h+=$(i[j]).outerWidth(!0);c.animate({scrollLeft:Math.max(0,h-(e-f)/2)},500)}$("ul.nav-tabs a").click(function(){$(this).tab("show")});var b=window.location.href;$(".policies-tile .nav-tabs a").click(function(a){a.preventDefault();var c=$(this).attr("href").substring(1);b.indexOf("index_html")>-1?(b=b.replace("index_html",c),document.location=b):document.location=b+"/"+c}),$(".policies-dynamic-area a").click(function(a){a.preventDefault();var b=$(this).attr("href");document.location=b}),$(".main-nav-tabs li a").click(function(){var b=$(this).parent();a(b,".main-nav-tabs")})}function rotateActiveTab(){window.initCountriesMapTile&&initCountriesMapTile()}function qtip2Initializer(){$('a[href*="glossary#link"]').each(function(){var a=this,b=$(this).attr("href"),c=b.substring(b.indexOf("#")+1);$(this).addClass("glossary-inline-term"),$(a).qtip({content:{text:function(b,d){var e=$(a).text();return $.ajax({url:$(a).attr("href")}).then(function(a){var b=$(a).find("#"+c);d.set("content.text",b)},function(a,b,c){d.set("content.text",b+": "+c)}),'<div class="GlossaryTitle">'+e.charAt(0).toUpperCase()+e.slice(1)+"</div><p>Loading glossary term...</p>"}},position:{at:"bottom center",my:"top center",viewport:$(window),effect:!1},show:{event:"mouseenter",solo:!0},hide:{event:"mouseleave"},style:{classes:"ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded"}})})}function initAst(){function a(){if(c){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var d=$(".ast-title-step").text();0==d&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===d&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F","font-family":"OpenSansB"})})}$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #fff",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#8A9C3A",border:"2px solid #fff",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})});var b=$(".subsection-tools-urban-ast h2");b.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var c=$(".subsection-tools-adaptation-support-tool").length>0,d=$(".subsection-tools-urban-ast").length>0;d&&$(".cover-richtext-tile ul li a").attr("target","_blank");var e=window.location.pathname,f=window.location.pathname.split("/"),g=$("#document-action-download_pdf"),h='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';e.indexOf("/tools/urban-ast")!==-1&&e.indexOf("pdf.body")===-1&&(f.pop(),f=f.join("/")+"/ast.pdf",h=h.replace("{0}",f),g.parent().before(h)),e.indexOf("/tools/adaptation-support-tool")!==-1&&e.indexOf("pdf.body")===-1&&(f.pop(),f=f.join("/")+"/ast.pdf",h=h.replace("{0}",f),g.parent().before(h));var i=$("#uast-image-map").children("area");i.each(function(){this.href=this.href.replace("/tools","/knowledge/tools")}),$(".acecontent_filtering_tile select").on("change",function(){$(this).parents("form").submit()}),$(".sub-menu-link").each(function(){var a=$(this);a.attr("href")||(a.hover(function(){a.css("color","#3a3a3a")}),a.css("color","#3a3a3a"))}),a()}function initMobileMenu(){function a(){var a=$(this).scrollTop();Math.abs(e-a)<=f||(a>e&&a>g?$(".top-menu").removeClass("nav-down").addClass("nav-up"):a+$(window).height()<$(document).height()&&$(".top-menu").removeClass("nav-up").addClass("nav-down"),e=a)}var b=$("body");$(".mobile-menu i").click(function(){return b.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1});var c=/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);c&&$(".main-nav-item").each(function(){var a=$(this),b=a.find(".main-nav-link");b.attr("href")||a.click(function(){b.parent().siblings(".sub-menu-wrapper").toggle(),b.parent().parent().siblings().find(".sub-menu-wrapper").hide()})});var d,e=0,f=5,g=$(".top-menu").outerHeight(),h=$(window).width();$(window).scroll(function(){d=!0,h<=800&&($(window).scrollTop()>=80?$(".header").addClass("sticky-header"):$(".header").removeClass("sticky-header"))}),h<=800&&setInterval(function(){d&&(a(),d=!1)},250)}function initMainNavMenu(){var a=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var b=$(this),c=b.children(".sub-menu-wrapper").width();if(b.find(".sub-menu-wrapper").length>0)var d=b.children(".sub-menu-wrapper").offset().left;a-(c+d)<0&&b.children(".sub-menu-wrapper").css({right:0,left:"auto"})})}function initExternalLinks(){$("a").each(function(){var a=$(this),b=0==a.parents(".header").length;if(b){var c=new RegExp("/"+window.location.host+"/");c.test(this.href)||a.attr("target","_blank")}})}function fixForms(){var a=$("input[type=submit]");a.each(function(){var a=$(this);a.val().match(/^(Save|Activate|Deactivate|Update subscriptions|Apply Changes)$/i)?a.addClass("standard-button primary-button"):"Cancel"===a.val()?a.addClass("standard-button secondary-button"):a.addClass("standard-button secondary-button")}),$("select").addClass("form-control")}function initCountryPages(){var a,b=$(".subsection-sector-policies").length>0;if(b){var c=$(".read_more_second").children("h2");c.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))}),a=$(".column.col-md-3"),a.before(a.find(".factsheet-pdf").parent()),$(".factsheet-pdf").parent().css("text-decoration","none")}a=$(".subsection-transnational-regions .column.col-md-3"),a.after(a.find(".detailed-content").parentsUntil(".tile-default")),$(".country-header").closest("#content").addClass("country-profile-content"),$(".country-select-tile").closest(".row").css("margin","0"),$(".country-profile-content .sweet-tabs").attr("id","country-tab");var d=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){d.find(".selected").html($(this).text()),d.find(".selected-inp").val($(this).data("value")).trigger("change"),d.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){d.find(".options").fadeToggle().toggleClass("show"),d.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text().replace(" ","-");c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}function fixMoveMap(){var a=$(".speedbutton");if(a.length>0){var b=$(".col-md-3.content-sidebar"),c=a.closest(".tile-default").addClass("interactive-map-wrapper");c.prev().addClass("map-list-wrapper"),$(".interactive-map-wrapper, .map-list-wrapper").wrapAll('<div class="interactive-maps" />');var d=$(".interactive-maps");b.after(b.find(d))}}function fixUseCases(){var a=$(".use-cases-listing tbody tr");a.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")})}function initCustomAccordions(){var a=$(".panel-title a");a.addClass("arrow-down"),a.click(function(){$(this).toggleClass("arrow-up arrow-down")}),$(".tile").each(function(){var a=$(this);a.hasClass("classic-accordion")||a.find(".panel-default").closest(".cover-richtext-tile").addClass("custom-accordion")});var b=$(".custom-accordion"),c=b.find(".panel-heading"),d=b.find(".panel-collapse"),e=b.find(".panel-default");a.click(function(){var a=$(this);"Read more"===a.text()?a.text("Read less"):"Read less"===a.text()&&a.text("Read more")}),d.css({display:"block",height:"100px",overflow:"hidden",position:"relative"}),c.css("text-align","right");var f=$('<div class="panel-layer fadein"/>');d.prepend(f),e.each(function(){var a=$(".panel-title a",this),b=$(".panel-collapse",this),c=$(".panel-layer",this);$(".panel-heading",this).before(b);var d=!1;a.on("click",function(){d?(b.removeClass("panel-opened"),c.removeClass("fadeout").addClass("fadein"),d=!1):(b.addClass("panel-opened"),c.removeClass("fadein").addClass("fadeout"),d=!0)})})}function fixTiles(){$(".tile-container").each(function(){var a=$(this),b=a.children("a"),c=a.children("div");"Edit"==b.text()&&b.detach().appendTo(c)}),$(".template-compose .tile").each(function(){var a=$(this);a.hasClass("col-md-4")?(a.removeClass("col-md-4"),a.parent(".tile-container").addClass("col-md-4")):a.hasClass("col-md-6")&&(a.removeClass("col-md-6"),a.parent(".tile-container").addClass("col-md-6"))}),$(".col-md-6, .col-md-4").each(function(){var a=$(this);a.find(".cover-richtext-tile").children("h2").addClass("richtext-tile-title"),$(".richtext-tile-title").parent().css("padding","0 .5em")})}function fixPDFButton(){var a=$("#document-action-download_pdf");a.parent().wrapAll('<div class="documentExportActions"/>');var b=$(".documentExportActions"),c=$(".content-column").length>0,d=$(".country-header").length>0;c?$(".content-column").append(b):d?($(".tab-content").append(b),b.css({"float":"none",display:"inline-block"})):($("#content").append(b),b.css({"float":"none",display:"inline-block"})),window.location.href.indexOf("data-and-downloads")>-1&&a.parent().hide()}function fixGallery(){$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}});var a=$(".aceitem_page .col-md-3");a.before(a.find(".case-studies-illustrations")),a.before(a.find(".sidebar_files")),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var b=$("#links");b.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var c=b.children(".gallery-hide").length;b.children(".gallery-hide").slice(1,c).css("display","none")}})}$(document).ready(function(){function a(){b(),c()}var b=initSlider(),c=initMainArea();initMainTabs(),initAst(),initMobileMenu(),initMainNavMenu(),initExternalLinks(),initCountryPages(),initCustomAccordions(),fixTiles(),fixForms(),fixMoveMap(),fixUseCases(),fixPDFButton(),fixGallery(),rotateActiveTab(),window.require&&window.requirejs&&(window.requirejs.config({paths:{qtip2:"//cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/jquery.qtip.min"}}),window.requirejs(["qtip2"],qtip2Initializer));var d;$(window).resize(function(){clearTimeout(d),d=setTimeout(a,500)}),$(".policies-nav a").hover(function(){$(this).tab("show")}),$("#user-name").click(function(a){a.preventDefault()}),$(".CSSTableGenerator").addClass("listing"),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button");var e=$(".bluebutton");e.addClass("standard-button primary-button"),e.parent().css("text-align","left"),$("#document-action-rss").parent().hide();var f=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(f.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(f)>-1)&&a.addClass("active-nav")});var g=$(window).width();g<=800&&$("#main-nav-item-3").children(".sub-menu-wrapper").append($('<div class="mobile-clearfix"/>')),$('#search-field input[type="text"]').attr("placeholder","type here..."),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var h=$(".tile");h.each(function(){var a=$(this);0===a.children().length&&a.hide()}),$(".row.container-themes .col-md-3").click(function(){console.log($(this).attr("data-url")),void 0!==$(this).attr("data-url")&&(window.location=$(this).attr("data-url"))})});