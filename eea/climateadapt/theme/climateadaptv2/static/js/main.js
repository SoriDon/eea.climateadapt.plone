$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){h.find(".pause").css("left",function(){return a()+3+"px"}),h.find(".pause-circle").css("left",function(){return a()+"px"}),i.css("right",function(){return a()+"px"}),j.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){if(z){$(".country-select-tile").closest(".row").css("margin","0"),$(".sweet-tabs").attr("id","country-tab");var a=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){a.find(".selected").html($(this).text()),a.find(".selected-inp").val($(this).data("value")).trigger("change"),a.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(b){a.find(".options").fadeToggle().toggleClass("show"),a.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),b.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList()}}function e(){if(A){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F"})})}function f(){$('a[href*="glossary#link"]').each(function(){var a=this,b=$(this).attr("href"),c=b.substring(b.indexOf("#")+1);$(this).addClass("glossary-inline-term"),$(a).qtip({content:{text:function(b,d){var e=$(a).text();return $.ajax({url:$(a).attr("href")}).then(function(a){var b=$(a).find("#"+c);d.set("content.text",b)},function(a,b,c){d.set("content.text",b+": "+c)}),'<div class="GlossaryTitle">'+e.charAt(0).toUpperCase()+e.slice(1)+"</div><p>Loading glossary term...</p>"}},position:{at:"bottom center",my:"top center",viewport:$(window),effect:!1},show:{event:"mouseenter",solo:!0},hide:{event:"mouseleave"},style:{classes:"ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded"}})})}var g=$("body");$(".slider").slick&&($(".slider-for").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3}),$(".slider-nav a").click(function(a){a.preventDefault();var b=$(this).index();$(".slider-for").slick("slickGoTo",parseInt(b)),$(".slider-for").slick("slickPlay")}),$(".slider-for").on("setPosition",function(){var a=$(".slider-for").slick("slickCurrentSlide")+1;$(".slider-nav a").removeClass("active-slider"),$(".slider-nav a:nth-child("+a+")").addClass("active-slider")}),$(".pause").on("click",function(){$(".slider-for").slick("slickPause")}));var h=$(".slider"),i=$(".slider-caption"),j=$(".slider-nav");h.find(".pause").css("left",function(){return a()+3+"px"}),h.find(".pause-circle").css("left",function(){return a()+"px"}),i.css("right",function(){return a()+"px"}),j.css("right",function(){return a()+"px"});var k;$(window).resize(function(){clearTimeout(k),k=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".policies-tile .nav-tabs a").hover(function(){$(this).tab("show")});var l=window.location.href;$(".policies-tile .nav-tabs a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);l.indexOf("index_html")>-1?(l=l.replace("index_html",b),document.location=l):document.location=l+"/"+b}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-tab-heading .main-nav-tabs")}),$(".action-btn").each(function(){var a=$(this);a.hover(function(){a.hasClass("regional-btn")&&a.siblings(".action-bubble").toggleClass("regional-bubble"),a.hasClass("transnational-btn")&&a.siblings(".action-bubble").toggleClass("transnational-bubble"),a.hasClass("national-btn")&&a.siblings(".action-bubble").toggleClass("national-bubble")})}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #F2C94C",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#8A9C3A",border:"2px solid #788833",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".close-tab-pane").click(function(){var a=$(this).closest(".policies-tab-content"),b=$(this).closest(".sub-tab-section");b.find(".action-flex-item").removeClass("active"),a.removeClass("active")});var m=$(window).width(),n=$(".main-box"),o=0;n.each(function(){o=$(this).outerHeight()>o?$(this).outerHeight():o}),m<=767?n.css("min-height","auto"):n.css("min-height",o),$(".mobile-menu i").click(function(){return g.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".toggle-down").click(function(){return $(this).parent().siblings(".sub-menu-wrapper").toggle(),$(this).parent().parent().siblings().children(".sub-menu-wrapper").hide(),!1}),$("#user-name").click(function(a){a.preventDefault()});var p=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;p-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})}),$(".CSSTableGenerator").addClass("listing"),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button");var q=$(".bluebutton");q.addClass("standard-button primary-button"),q.parent().css("text-align","left");var r=$("input[type=submit]");r.each(function(){var a=$(this);a.val().match(/^(Save|Activate|Deactivate|Update subscriptions|Apply Changes)$/i)?a.addClass("standard-button primary-button"):"Cancel"===a.val()?a.addClass("standard-button secondary-button"):a.addClass("standard-button secondary-button")}),$("select").addClass("form-control");var s=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(s.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(s)>-1)&&a.addClass("active-nav")});var t,u=window.location.pathname,v=u.split("/");t=0===v[v.length-1].length?v[v.length-2]:v[v.length-1],t="index_html"===t?v[v.length-3]:v[v.length-1];var w="subsection-countries-"+t,x=void 0!==g.attr("class")?g.attr("class").split(/\s+/):[];$.each(x,function(a,b){b===w&&g.addClass("country-page")});var y=$(".subsection-sector-policies").length>0,z=$(".country-page").length>0,A=$(".subsection-tools-adaptation-support-tool").length>0;if(y){var B=$(".read_more_second").children("h2");B.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var C=$(".column.col-md-3");C.before(C.find(".factsheet-pdf").parent())}var C=$(".subsection-transnational-regions .column.col-md-3");C.after(C.find(".detailed-content").parentsUntil(".tile-default")),d(),e(),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),m<=800&&$("#main-nav-item-3").children(".sub-menu-wrapper").append($('<div class="mobile-clearfix"/>')),$('#search-field input[type="text"]').attr("placeholder","type here...");var D=$(".subsection-tools-urban-ast h2");D.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var E=$(".subsection-tools-urban-ast").length>0;E&&$(".cover-richtext-tile ul li a").attr("target","_blank");var F=$("#document-action-download_pdf");F.parent().wrapAll('<div class="documentExportActions"/>');var G=$(".documentExportActions"),H=$(".content-column").length>0;if(H?$(".content-column").append(G):z?($(".tab-content").append(G),G.css({"float":"none",display:"inline-block"})):($("#content").append(G),G.css({"float":"none",display:"inline-block"})),u.indexOf("/tools/urban-ast")!==-1&&u.indexOf("pdf.body")===-1){var I='<a href="/tools/urban-ast/download.pdf"class="standard-button ast-section-pdf">Download section as PDF</a>';F.parent().before(I)}if(u.indexOf("/tools/adaptation-support-tool")!==-1&&u.indexOf("pdf.body")===-1){var I='<a href="/tools/adaptation-support-tool/download.pdf"class="standard-button ast-section-pdf">Download section as PDF</a>';F.parent().before(I)}$(".tile-container").each(function(){var a=$(this),b=a.children("a"),c=a.children("div");"Edit"==b.text()&&b.detach().appendTo(c)});var J=$(".panel-title a");J.click(function(){$(this).text(function(a,b){return"Read more"===b?"Read less":"Read more"})}),$(".panel-heading").before($(".panel-collapse"));var K=$('<div class="panel-layer fadein"/>');$(".panel-collapse").prepend(K);var L=J.closest(".panel-heading").siblings();L.addClass("panel-opened"),J.toggle(function(){L.addClass("panel-opened"),L.children(".panel-layer").removeClass("fadein").addClass("fadeout")},function(){L.removeClass("panel-opened"),L.children(".panel-layer").removeClass("fadeout").addClass("fadein")}),window.location.href.indexOf("data-and-downloads")>-1&&F.parent().hide();var M=$(".speedbutton");if(M.length>0){var C=$(".col-md-3.content-sidebar"),N=M.closest(".tile-default").addClass("interactive-map-wrapper");N.prev().addClass("map-list-wrapper");$(".interactive-map-wrapper, .map-list-wrapper").wrapAll('<div class="interactive-maps" />');var O=$(".interactive-maps");C.after(C.find(O))}var P=$("#links");P.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var b=P.children(".gallery-hide").length;P.children(".gallery-hide").slice(1,b).css("display","none")}}),$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}}),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var Q=$(".aceitem_page .col-md-3");Q.before(Q.find(".case-studies-illustrations")),Q.before(Q.find(".sidebar_files"));var R=$(".use-cases-listing tbody tr");R.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")}),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var S=$(".subsection-tools-urban-adaptation-climatic-threats").length>0;S&&g.addClass("fullwidth");var T=$(".tile");T.each(function(){$this=$(this),0===$this.children().length&&$this.hide()}),$("a").each(function(){var a=new RegExp("/"+window.location.host+"/");a.test(this.href)||$(this).attr("target","_blank")}),window.require&&window.requirejs&&(requirejs.config({paths:{qtip2:"//cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/jquery.qtip.min"}}),requirejs(["qtip2"],f))});