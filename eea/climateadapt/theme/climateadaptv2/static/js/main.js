$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){i.css("right",function(){return a()+"px"}),j.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){var a=$(this).scrollTop();Math.abs(q-a)<=r||(a>q&&a>s?$(".top-menu").removeClass("nav-down").addClass("nav-up"):a+$(window).height()<$(document).height()&&$(".top-menu").removeClass("nav-up").addClass("nav-down"),q=a)}function e(){if(z){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F","font-family":"OpenSansB"})})}function f(){var a=$(".panel-heading"),b=$(".panel-collapse");L.click(function(){$(this).text(function(a,b){return"Read more"===b?"Read less":"Read more"})}),b.css({display:"block",height:"130px",overflow:"hidden",position:"relative"}),a.css("text-align","right"),a.before(b);var c=$('<div class="panel-layer fadein"/>');b.prepend(c);var d=L.closest(".panel-heading").siblings();L.toggle(function(){d.addClass("panel-opened"),d.children(".panel-layer").removeClass("fadein").addClass("fadeout")},function(){d.removeClass("panel-opened"),d.children(".panel-layer").removeClass("fadeout").addClass("fadein")})}function g(){$('a[href*="glossary#link"]').each(function(){var a=this,b=$(this).attr("href"),c=b.substring(b.indexOf("#")+1);$(this).addClass("glossary-inline-term"),$(a).qtip({content:{text:function(b,d){var e=$(a).text();return $.ajax({url:$(a).attr("href")}).then(function(a){var b=$(a).find("#"+c);d.set("content.text",b)},function(a,b,c){d.set("content.text",b+": "+c)}),'<div class="GlossaryTitle">'+e.charAt(0).toUpperCase()+e.slice(1)+"</div><p>Loading glossary term...</p>"}},position:{at:"bottom center",my:"top center",viewport:$(window),effect:!1},show:{event:"mouseenter",solo:!0},hide:{event:"mouseleave"},style:{classes:"ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded"}})})}var h=$("body");$(".slider").slick&&($(".slider-for").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3}),$(".slider-nav a").click(function(a){a.preventDefault();var b=$(this).index();$(".slider-for").slick("slickGoTo",parseInt(b))}),$(".slider-nav a").mouseenter(function(a){$(".slider-for").slick("slickPause")}).mouseleave(function(){$(".slider-for").slick("slickPlay")}),$(".slider-for").on("setPosition",function(){var a=$(".slider-for").slick("slickCurrentSlide")+1;$(".slider-nav a").removeClass("active-slider"),$(".slider-nav a:nth-child("+a+")").addClass("active-slider")}));var i=($(".slider"),$(".slider-caption")),j=$(".slider-nav");i.css("right",function(){return a()+"px"}),j.css("right",function(){return a()+"px"});var k;$(window).resize(function(){clearTimeout(k),k=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".policies-nav a").hover(function(){$(this).tab("show")});var l=window.location.href;$(".policies-tile .nav-tabs a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);l.indexOf("index_html")>-1?(l=l.replace("index_html",b),document.location=l):document.location=l+"/"+b}),$(".policies-dynamic-area a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);document.location=l+"/eu-adaptation-policy/sector-policies/"+b}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-nav-tabs")}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #fff",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#8A9C3A",border:"2px solid #fff",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})});var m=$(window).width(),n=$(".main-box"),o=0;n.each(function(){o=$(this).outerHeight()>o?$(this).outerHeight():o}),m<=767?n.css("min-height","auto"):n.css("min-height",o),$(".mobile-menu i").click(function(){return h.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".toggle-down").click(function(){return $(this).parent().siblings(".sub-menu-wrapper").toggle(),$(this).parent().parent().siblings().children(".sub-menu-wrapper").hide(),!1});var p,q=0,r=5,s=$(".top-menu").outerHeight();$(window).scroll(function(a){p=!0,m<=800&&($(window).scrollTop()>=80?$(".header").addClass("sticky-header"):$(".header").removeClass("sticky-header"))}),m<=800&&setInterval(function(){p&&(d(),p=!1)},250),$("#user-name").click(function(a){a.preventDefault()});var t=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;t-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})}),$(".CSSTableGenerator").addClass("listing"),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button");var u=$(".bluebutton");u.addClass("standard-button primary-button"),u.parent().css("text-align","left");var v=$("input[type=submit]");v.each(function(){var a=$(this);a.val().match(/^(Save|Activate|Deactivate|Update subscriptions|Apply Changes)$/i)?a.addClass("standard-button primary-button"):"Cancel"===a.val()?a.addClass("standard-button secondary-button"):a.addClass("standard-button secondary-button")}),$("select").addClass("form-control");var w=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(w.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(w)>-1)&&a.addClass("active-nav")});var x=window.location.pathname,y=$(".subsection-sector-policies").length>0,z=$(".subsection-tools-adaptation-support-tool").length>0;if(y){var A=$(".read_more_second").children("h2");A.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var B=$(".column.col-md-3");B.before(B.find(".factsheet-pdf").parent()),$(".factsheet-pdf").parent().css("text-decoration","none")}var B=$(".subsection-transnational-regions .column.col-md-3");B.after(B.find(".detailed-content").parentsUntil(".tile-default")),$(".country-header").closest("#content").addClass("country-profile-content"),$(".country-select-tile").closest(".row").css("margin","0"),$(".country-profile-content .sweet-tabs").attr("id","country-tab");var C=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){C.find(".selected").html($(this).text()),C.find(".selected-inp").val($(this).data("value")).trigger("change"),C.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){C.find(".options").fadeToggle().toggleClass("show"),C.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList(),e(),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),m<=800&&$("#main-nav-item-3").children(".sub-menu-wrapper").append($('<div class="mobile-clearfix"/>')),$('#search-field input[type="text"]').attr("placeholder","type here...");var D=$(".subsection-tools-urban-ast h2");D.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var E=$(".subsection-tools-urban-ast").length>0;E&&$(".cover-richtext-tile ul li a").attr("target","_blank");var F=$("#document-action-download_pdf");F.parent().wrapAll('<div class="documentExportActions"/>');var G=$(".documentExportActions"),H=$(".content-column").length>0,I=$(".country-header").length>0;if(H?$(".content-column").append(G):I?($(".tab-content").append(G),G.css({"float":"none",display:"inline-block"})):($("#content").append(G),G.css({"float":"none",display:"inline-block"})),x.indexOf("/tools/urban-ast")!==-1&&x.indexOf("pdf.body")===-1){var J=window.location.pathname.split("/");J.pop(),J=J.join("/")+"/ast.pdf";var K='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';K=K.replace("{0}",J),F.parent().before(K)}if(x.indexOf("/tools/adaptation-support-tool")!==-1&&x.indexOf("pdf.body")===-1){var J=window.location.pathname.split("/");J.pop(),J=J.join("/")+"/ast.pdf";var K='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';K=K.replace("{0}",J),F.parent().before(K)}$(".tile-container").each(function(){var a=$(this),b=a.children("a"),c=a.children("div");"Edit"==b.text()&&b.detach().appendTo(c)}),$(".template-compose .tile").each(function(){var a=$(this);a.hasClass("col-md-4")?(a.removeClass("col-md-4"),a.parent(".tile-container").addClass("col-md-4")):a.hasClass("col-md-6")&&(a.removeClass("col-md-6"),a.parent(".tile-container").addClass("col-md-6"))}),$(".col-md-6, .col-md-4").each(function(){var a=$(this);a.find(".cover-richtext-tile").children("h2").addClass("richtext-tile-title"),$(".richtext-tile-title").parent().css("padding","0 .5em")});var L=$(".panel-title a");L.addClass("arrow-down"),L.click(function(){$(this).toggleClass("arrow-up arrow-down")});var M=$(".subsection-adaptation-information-research-projects").length>0,N=$(".subsection-organisations").length>0,O=M||N;O||f(),window.location.href.indexOf("data-and-downloads")>-1&&F.parent().hide();var P=$(".speedbutton");if(P.length>0){var B=$(".col-md-3.content-sidebar"),Q=P.closest(".tile-default").addClass("interactive-map-wrapper");Q.prev().addClass("map-list-wrapper");$(".interactive-map-wrapper, .map-list-wrapper").wrapAll('<div class="interactive-maps" />');var R=$(".interactive-maps");B.after(B.find(R))}var S=$("#links");S.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var b=S.children(".gallery-hide").length;S.children(".gallery-hide").slice(1,b).css("display","none")}}),$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}}),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var T=$(".aceitem_page .col-md-3");T.before(T.find(".case-studies-illustrations")),T.before(T.find(".sidebar_files"));var U=$(".use-cases-listing tbody tr");U.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")}),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var V=$(".subsection-tools-urban-adaptation-climatic-threats").length>0;V&&h.addClass("fullwidth");var W=$(".tile");W.each(function(){$this=$(this),0===$this.children().length&&$this.hide()}),$("a").each(function(){var a=new RegExp("/"+window.location.host+"/");a.test(this.href)||$(this).attr("target","_blank")});var X=$("#uast-image-map").children("area");X.each(function(){this.href=this.href.replace("/tools","/knowledge/tools")}),$(".acecontent_filtering_tile select").on("change",function(a){$(this).parents("form").submit()}),$(".sub-menu-link").each(function(){var a=$(this);a.attr("href")||a.hover(function(){a.css("color","#005C96")})}),window.require&&window.requirejs&&(requirejs.config({paths:{qtip2:"//cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/jquery.qtip.min"}}),requirejs(["qtip2"],g))});