$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){$(".slider-caption, .slider-nav").css("right",function(){return a()+"px"}),$(".image-copyright").css("left",function(){return a()+"px"}),$(this).width()>=767?j.css("height",k):j.css("height","")}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){var a=$(this).scrollTop();Math.abs(p-a)<=q||(a>p&&a>r?$(".top-menu").removeClass("nav-down").addClass("nav-up"):a+$(window).height()<$(document).height()&&$(".top-menu").removeClass("nav-up").addClass("nav-down"),p=a)}function e(){if(y){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F","font-family":"OpenSansB"})})}function f(){$('a[href*="glossary#link"]').each(function(){var a=this,b=$(this).attr("href"),c=b.substring(b.indexOf("#")+1);$(this).addClass("glossary-inline-term"),$(a).qtip({content:{text:function(b,d){var e=$(a).text();return $.ajax({url:$(a).attr("href")}).then(function(a){var b=$(a).find("#"+c);d.set("content.text",b)},function(a,b,c){d.set("content.text",b+": "+c)}),'<div class="GlossaryTitle">'+e.charAt(0).toUpperCase()+e.slice(1)+"</div><p>Loading glossary term...</p>"}},position:{at:"bottom center",my:"top center",viewport:$(window),effect:!1},show:{event:"mouseenter",solo:!0},hide:{event:"mouseleave"},style:{classes:"ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded"}})})}var g=$("body");if($(".slider").slick){$(".slider-for").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var h=$(".slider-thumb");h.click(function(a){a.preventDefault();var b=$(this).index();$(".slider-for").slick("slickGoTo",parseInt(b))}),h.mouseenter(function(a){$(".slider-for").slick("slickPause")}).mouseleave(function(){$(".slider-for").slick("slickPlay")}),$(".slider-for").on("setPosition",function(){var a=$(".slider-for").slick("slickCurrentSlide")+1;h.removeClass("active-slider"),$(".slider-thumb:nth-child("+a+")").addClass("active-slider")})}setTimeout(function(){$(".slider-caption, .slider-nav, .image-copyright").fadeIn(700)},200);$(".slider");$(".slider-caption, .slider-nav").css("right",function(){return a()+"px"}),$(".image-copyright").css("left",function(){return a()+"px"});var i=$(window).width(),j=$(".main-box"),k=0;j.each(function(){k=$(this).outerHeight()>k?$(this).outerHeight():k}),i>=767?j.css("height",k):j.css("height","");var l;$(window).resize(function(){clearTimeout(l),l=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show")}),$(".policies-nav a").hover(function(){$(this).tab("show")});var m=window.location.href;$(".policies-tile .nav-tabs a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);m.indexOf("index_html")>-1?(m=m.replace("index_html",b),document.location=m):document.location=m+"/"+b}),$(".policies-dynamic-area a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);document.location=m+"/eu-adaptation-policy/sector-policies/"+b}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-nav-tabs")}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #fff",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#8A9C3A",border:"2px solid #fff",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})}),$(".mobile-menu i").click(function(){return g.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1});var n=/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);n&&$(".main-nav-item").each(function(){var a=$(this),b=a.find(".main-nav-link");b.attr("href")||a.click(function(){b.parent().siblings(".sub-menu-wrapper").toggle(),b.parent().parent().siblings().find(".sub-menu-wrapper").hide()})});var o,p=0,q=5,r=$(".top-menu").outerHeight();$(window).scroll(function(a){o=!0,i<=800&&($(window).scrollTop()>=80?$(".header").addClass("sticky-header"):$(".header").removeClass("sticky-header"))}),i<=800&&setInterval(function(){o&&(d(),o=!1)},250),$("#user-name").click(function(a){a.preventDefault()});var s=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;s-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})}),$(".CSSTableGenerator").addClass("listing"),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button");var t=$(".bluebutton");t.addClass("standard-button primary-button"),t.parent().css("text-align","left");var u=$("input[type=submit]");u.each(function(){var a=$(this);a.val().match(/^(Save|Activate|Deactivate|Update subscriptions|Apply Changes)$/i)?a.addClass("standard-button primary-button"):"Cancel"===a.val()?a.addClass("standard-button secondary-button"):a.addClass("standard-button secondary-button")}),$("select").addClass("form-control"),$("#document-action-rss").parent().hide();var v=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(v.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(v)>-1)&&a.addClass("active-nav")});var w=window.location.pathname,x=$(".subsection-sector-policies").length>0,y=$(".subsection-tools-adaptation-support-tool").length>0;if(x){var z=$(".read_more_second").children("h2");z.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var A=$(".column.col-md-3");A.before(A.find(".factsheet-pdf").parent()),$(".factsheet-pdf").parent().css("text-decoration","none")}var A=$(".subsection-transnational-regions .column.col-md-3");A.after(A.find(".detailed-content").parentsUntil(".tile-default")),$(".country-header").closest("#content").addClass("country-profile-content"),$(".country-select-tile").closest(".row").css("margin","0"),$(".country-profile-content .sweet-tabs").attr("id","country-tab");var B=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){B.find(".selected").html($(this).text()),B.find(".selected-inp").val($(this).data("value")).trigger("change"),B.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){B.find(".options").fadeToggle().toggleClass("show"),B.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text().replace(" ","-");c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList(),e(),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),i<=800&&$("#main-nav-item-3").children(".sub-menu-wrapper").append($('<div class="mobile-clearfix"/>')),$('#search-field input[type="text"]').attr("placeholder","type here...");var C=$(".subsection-tools-urban-ast h2");C.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var D=$(".subsection-tools-urban-ast").length>0;D&&$(".cover-richtext-tile ul li a").attr("target","_blank");var E=$("#document-action-download_pdf");E.parent().wrapAll('<div class="documentExportActions"/>');var F=$(".documentExportActions"),G=$(".content-column").length>0,H=$(".country-header").length>0;if(G?$(".content-column").append(F):H?($(".tab-content").append(F),F.css({"float":"none",display:"inline-block"})):($("#content").append(F),F.css({"float":"none",display:"inline-block"})),w.indexOf("/tools/urban-ast")!==-1&&w.indexOf("pdf.body")===-1){var I=window.location.pathname.split("/");I.pop(),I=I.join("/")+"/ast.pdf";var J='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';J=J.replace("{0}",I),E.parent().before(J)}if(w.indexOf("/tools/adaptation-support-tool")!==-1&&w.indexOf("pdf.body")===-1){var I=window.location.pathname.split("/");I.pop(),I=I.join("/")+"/ast.pdf";var J='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';J=J.replace("{0}",I),E.parent().before(J)}$(".tile-container").each(function(){var a=$(this),b=a.children("a"),c=a.children("div");"Edit"==b.text()&&b.detach().appendTo(c)}),$(".template-compose .tile").each(function(){var a=$(this);a.hasClass("col-md-4")?(a.removeClass("col-md-4"),a.parent(".tile-container").addClass("col-md-4")):a.hasClass("col-md-6")&&(a.removeClass("col-md-6"),a.parent(".tile-container").addClass("col-md-6"))}),$(".col-md-6, .col-md-4").each(function(){var a=$(this);a.find(".cover-richtext-tile").children("h2").addClass("richtext-tile-title"),$(".richtext-tile-title").parent().css("padding","0 .5em")});var K=$(".panel-title a");K.addClass("arrow-down"),K.click(function(){$(this).toggleClass("arrow-up arrow-down")}),$(".tile").each(function(){var a=$(this);a.hasClass("classic-accordion")||a.find(".panel-default").closest(".cover-richtext-tile").addClass("custom-accordion")});var L=$(".custom-accordion"),M=L.find(".panel-heading"),N=L.find(".panel-collapse"),O=L.find(".panel-default");K.click(function(){var a=$(this);"Read more"===a.text()?a.text("Read less"):"Read less"===a.text()&&a.text("Read more")}),N.css({display:"block",height:"100px",overflow:"hidden",position:"relative"}),M.css("text-align","right");var P=$('<div class="panel-layer fadein"/>');N.prepend(P),O.each(function(){var a=$(".panel-title a",this),b=$(".panel-collapse",this),c=$(".panel-layer",this);$(".panel-heading",this).before(b),a.toggle(function(){b.addClass("panel-opened"),c.removeClass("fadein").addClass("fadeout")},function(){b.removeClass("panel-opened"),c.removeClass("fadeout").addClass("fadein")})}),window.location.href.indexOf("data-and-downloads")>-1&&E.parent().hide();var Q=$(".speedbutton");if(Q.length>0){var A=$(".col-md-3.content-sidebar"),R=Q.closest(".tile-default").addClass("interactive-map-wrapper");R.prev().addClass("map-list-wrapper");$(".interactive-map-wrapper, .map-list-wrapper").wrapAll('<div class="interactive-maps" />');var S=$(".interactive-maps");A.after(A.find(S))}var T=$("#links");T.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var b=T.children(".gallery-hide").length;T.children(".gallery-hide").slice(1,b).css("display","none")}}),$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}}),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var U=$(".aceitem_page .col-md-3");U.before(U.find(".case-studies-illustrations")),U.before(U.find(".sidebar_files"));var V=$(".use-cases-listing tbody tr");V.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")}),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var W=$(".tile");W.each(function(){$this=$(this),0===$this.children().length&&$this.hide()}),$("a").each(function(){var a=$(this),b=0==a.parents(".header").length;if(b){var c=new RegExp("/"+window.location.host+"/");c.test(this.href)||a.attr("target","_blank")}});var X=$("#uast-image-map").children("area");X.each(function(){this.href=this.href.replace("/tools","/knowledge/tools")}),$(".acecontent_filtering_tile select").on("change",function(a){$(this).parents("form").submit()}),$(".sub-menu-link").each(function(){var a=$(this);a.attr("href")||(a.hover(function(){a.css("color","#3a3a3a")}),a.css("color","#3a3a3a"))}),window.require&&window.requirejs&&(requirejs.config({paths:{qtip2:"//cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/jquery.qtip.min"}}),requirejs(["qtip2"],f))});