$(document).ready(function(){function a(){var a=$(".content-container").width(),b=$(window).width(),c=(b-a)/2;return c}function b(){j.css("right",function(){return a()+"px"}),k.css("right",function(){return a()+"px"})}function c(a,b){for(var b=$(b),a=$(a),c=b.width(),d=a.outerWidth(!0),e=a.index(),f=0,g=b.find("li"),h=0;h<e;h++)f+=$(g[h]).outerWidth(!0);b.animate({scrollLeft:Math.max(0,f-(c-d)/2)},500)}function d(){var a=$(this).scrollTop();Math.abs(r-a)<=s||(a>r&&a>t?$(".top-menu").removeClass("nav-down").addClass("nav-up"):a+$(window).height()<$(document).height()&&$(".top-menu").removeClass("nav-up").addClass("nav-down"),r=a)}function e(){if(A){$(".col-md-8").children(".tile:nth-child(2)").addClass("tile-wrapper");var a=$(".tile-content").children("h1");a.each(function(){$("<h2>"+$(this).html()+"</h2>").replaceAll(this)}),$(".cover-richtext-tile ul li a").attr("target","_blank")}var b=$(".ast-map .ast-circle");b.hover(function(){$(this).siblings(".step-text").css("display","block")},function(){$(this).siblings(".step-text").css("display","none")});var c=$(".ast-title-step").text();0==c&&$(".ast-title-step").remove(),b.each(function(){$(this).text()===c&&$(this).css({"background-color":"#FFD554",border:"2px solid #F2C94C",color:"#4F4F4F","font-family":"OpenSansB"})})}function f(){var a=$(".panel-heading"),b=$(".panel-collapse");M.click(function(){$(this).text(function(a,b){return"Read more"===b?"Read less":"Read more"})}),b.css({display:"block",height:"130px",overflow:"hidden",position:"relative"}),a.css("text-align","right"),a.before(b);var c=$('<div class="panel-layer fadein"/>');b.prepend(c);var d=M.closest(".panel-heading").siblings();M.toggle(function(){d.addClass("panel-opened"),d.children(".panel-layer").removeClass("fadein").addClass("fadeout")},function(){d.removeClass("panel-opened"),d.children(".panel-layer").removeClass("fadeout").addClass("fadein")})}function g(){$('a[href*="glossary#link"]').each(function(){var a=this,b=$(this).attr("href"),c=b.substring(b.indexOf("#")+1);$(this).addClass("glossary-inline-term"),$(a).qtip({content:{text:function(b,d){var e=$(a).text();return $.ajax({url:$(a).attr("href")}).then(function(a){var b=$(a).find("#"+c);d.set("content.text",b)},function(a,b,c){d.set("content.text",b+": "+c)}),'<div class="GlossaryTitle">'+e.charAt(0).toUpperCase()+e.slice(1)+"</div><p>Loading glossary term...</p>"}},position:{at:"bottom center",my:"top center",viewport:$(window),effect:!1},show:{event:"mouseenter",solo:!0},hide:{event:"mouseleave"},style:{classes:"ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded"}})})}var h=$("body");if($(".slider").slick){$(".slider-for").slick({infinite:!0,speed:500,fade:!0,slidesToShow:1,dots:!0,autoplay:!0,autoplaySpeed:4e3});var i=$(".slider-thumb");i.click(function(a){a.preventDefault();var b=$(this).index();$(".slider-for").slick("slickGoTo",parseInt(b))}),i.mouseenter(function(a){$(".slider-for").slick("slickPause")}).mouseleave(function(){$(".slider-for").slick("slickPlay")}),$(".slider-for").on("setPosition",function(){var a=$(".slider-for").slick("slickCurrentSlide")+1;i.removeClass("active-slider"),$(".slider-thumb:nth-child("+a+")").addClass("active-slider")})}var j=($(".slider"),$(".slider-caption")),k=$(".slider-nav");j.css("right",function(){return a()+"px"}),k.css("right",function(){return a()+"px"});var l;$(window).resize(function(){clearTimeout(l),l=setTimeout(b,500)}),$("ul.nav-tabs a").click(function(a){$(this).tab("show"),a.preventDefault()}),$(".policies-nav a").hover(function(){$(this).tab("show")});var m=window.location.href;$(".policies-tile .nav-tabs a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);m.indexOf("index_html")>-1?(m=m.replace("index_html",b),document.location=m):document.location=m+"/"+b}),$(".policies-dynamic-area a").click(function(a){a.preventDefault();var b=$(this).attr("href"),b=b.substring(1);document.location=m+"/eu-adaptation-policy/sector-policies/"+b}),$(".main-nav-tabs li a").click(function(){var a=$(this).parent();c(a,".main-nav-tabs")}),$(".dynamic-area .ast-step-wrapper").hover(function(){$(this).children(".ast-circle").css({"background-color":"#FFD554",border:"2px solid #fff",transform:"scale(1.08)",color:"#4F4F4F"}),$(this).children(".step-text").css({"background-color":"#FFD554",transform:"scale(1.08)"})},function(){$(this).children(".ast-circle").css({"background-color":"#8A9C3A",border:"2px solid #fff",transform:"scale(1)",color:"#fff"}),$(this).children(".step-text").css({"background-color":"#f5f5f5",transform:"scale(1)"})});var n=$(window).width(),o=$(".main-box"),p=0;o.each(function(){p=$(this).outerHeight()>p?$(this).outerHeight():p}),n<=767?o.css("min-height","auto"):o.css("min-height",p),$(".mobile-menu i").click(function(){return h.toggleClass("no-ovf"),$(this).toggleClass("fa-bars fa-times"),$(".header").toggleClass("mobile-header"),$(".header .main-nav, .top-menu-content").toggleClass("nav-toggle"),!1}),$(".toggle-down").click(function(){return $(this).parent().siblings(".sub-menu-wrapper").toggle(),$(this).parent().parent().siblings().children(".sub-menu-wrapper").hide(),!1});var q,r=0,s=5,t=$(".top-menu").outerHeight();$(window).scroll(function(a){q=!0,n<=800&&($(window).scrollTop()>=80?$(".header").addClass("sticky-header"):$(".header").removeClass("sticky-header"))}),n<=800&&setInterval(function(){q&&(d(),q=!1)},250),$("#user-name").click(function(a){a.preventDefault()});var u=$(".main-nav-menu").width();$(".main-nav-menu li").mouseenter(function(){var a=$(this),b=a.children(".sub-menu-wrapper").width();if(a.find(".sub-menu-wrapper").length>0)var c=a.children(".sub-menu-wrapper").offset().left;u-(b+c)<0&&a.children(".sub-menu-wrapper").css({right:0,left:"auto"})}),$(".CSSTableGenerator").addClass("listing"),$("#document-action-download_pdf,#login-form .formControls input,#folderlisting-main-table .context").addClass("standard-button secondary-button");var v=$(".bluebutton");v.addClass("standard-button primary-button"),v.parent().css("text-align","left");var w=$("input[type=submit]");w.each(function(){var a=$(this);a.val().match(/^(Save|Activate|Deactivate|Update subscriptions|Apply Changes)$/i)?a.addClass("standard-button primary-button"):"Cancel"===a.val()?a.addClass("standard-button secondary-button"):a.addClass("standard-button secondary-button")}),$("select").addClass("form-control");var x=window.location.href;$(".share-info-wrapper #third-level-menu a, .cover-section_nav-tile a, .uvmb-nav a").each(function(){var a=$(this);(x.indexOf(a.attr("href"))>-1||a.attr("href").indexOf(x)>-1)&&a.addClass("active-nav")});var y=window.location.pathname,z=$(".subsection-sector-policies").length>0,A=$(".subsection-tools-adaptation-support-tool").length>0;if(z){var B=$(".read_more_second").children("h2");B.each(function(){$(this).replaceWith($("<p><strong>"+this.innerHTML+"</strong><p>"))});var C=$(".column.col-md-3");C.before(C.find(".factsheet-pdf").parent()),$(".factsheet-pdf").parent().css("text-decoration","none")}var C=$(".subsection-transnational-regions .column.col-md-3");C.after(C.find(".detailed-content").parentsUntil(".tile-default")),$(".country-header").closest("#content").addClass("country-profile-content"),$(".country-select-tile").closest(".row").css("margin","0"),$(".country-profile-content .sweet-tabs").attr("id","country-tab");var D=$(".dd-country-title");$(".dd-country-title .options li").on("click",function(){D.find(".selected").html($(this).text()),D.find(".selected-inp").val($(this).data("value")).trigger("change"),D.find(".options").removeClass("show")}),$(".dd-title-wrapper").on("click",function(a){D.find(".options").fadeToggle().toggleClass("show"),D.find("i").toggleClass("fa fa-angle-up fa fa-angle-down"),a.stopPropagation()}),$(".dd-country-title .selected-inp").on("change",function(a){var b=a.target.value,c=$(".dd-country-title li[data-value='"+b+"']").text();c.length&&(document.location="/countries/"+c.toLowerCase())}),$.fn.resizeselectList=function(a){return this.each(function(){$(this).change(function(){var a=$(this),b=a.parents().find(".dd-country-title .selected"),c=b.text(),d=$("<span/>").html(c).css({"font-size":b.css("font-size"),"font-weight":b.css("font-weight"),visibility:"hidden"});d.appendTo(a.parent());var e=d.width();d.remove(),a.width(e+45)}).change()})},$(".resizeselect-list").resizeselectList(),e(),$(".share-your-info-ace-button").wrapAll('<div class="clearfix"/>'),n<=800&&$("#main-nav-item-3").children(".sub-menu-wrapper").append($('<div class="mobile-clearfix"/>')),$('#search-field input[type="text"]').attr("placeholder","type here...");var E=$(".subsection-tools-urban-ast h2");E.each(function(){$(this).text().indexOf("Example cases:")>=0&&$(this).addClass("example-cases")});var F=$(".subsection-tools-urban-ast").length>0;F&&$(".cover-richtext-tile ul li a").attr("target","_blank");var G=$("#document-action-download_pdf");G.parent().wrapAll('<div class="documentExportActions"/>');var H=$(".documentExportActions"),I=$(".content-column").length>0,J=$(".country-header").length>0;if(I?$(".content-column").append(H):J?($(".tab-content").append(H),H.css({"float":"none",display:"inline-block"})):($("#content").append(H),H.css({"float":"none",display:"inline-block"})),y.indexOf("/tools/urban-ast")!==-1&&y.indexOf("pdf.body")===-1){var K=window.location.pathname.split("/");K.pop(),K=K.join("/")+"/ast.pdf";var L='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';L=L.replace("{0}",K),G.parent().before(L)}if(y.indexOf("/tools/adaptation-support-tool")!==-1&&y.indexOf("pdf.body")===-1){var K=window.location.pathname.split("/");K.pop(),K=K.join("/")+"/ast.pdf";var L='<a href="{0}" class="standard-button ast-section-pdf">Download section as PDF</a>';L=L.replace("{0}",K),G.parent().before(L)}$(".tile-container").each(function(){var a=$(this),b=a.children("a"),c=a.children("div");"Edit"==b.text()&&b.detach().appendTo(c)}),$(".template-compose .tile").each(function(){var a=$(this);a.hasClass("col-md-4")?(a.removeClass("col-md-4"),a.parent(".tile-container").addClass("col-md-4")):a.hasClass("col-md-6")&&(a.removeClass("col-md-6"),a.parent(".tile-container").addClass("col-md-6"))}),$(".col-md-6, .col-md-4").each(function(){var a=$(this);a.find(".cover-richtext-tile").children("h2").addClass("richtext-tile-title"),$(".richtext-tile-title").parent().css("padding","0 .5em")});var M=$(".panel-title a");M.addClass("arrow-down"),M.click(function(){$(this).toggleClass("arrow-up arrow-down")});var N=$(".subsection-adaptation-information-research-projects").length>0,O=$(".subsection-organisations").length>0,P=N||O;P||f(),window.location.href.indexOf("data-and-downloads")>-1&&G.parent().hide();var Q=$(".speedbutton");if(Q.length>0){var C=$(".col-md-3.content-sidebar"),R=Q.closest(".tile-default").addClass("interactive-map-wrapper");R.prev().addClass("map-list-wrapper");$(".interactive-map-wrapper, .map-list-wrapper").wrapAll('<div class="interactive-maps" />');var S=$(".interactive-maps");C.after(C.find(S))}var T=$("#links");T.children(".gallery-hide").eq(0).css("display","block"),$(document).keyup(function(a){if(27===a.keyCode){var b=T.children(".gallery-hide").length;T.children(".gallery-hide").slice(1,b).css("display","none")}}),$("#blueimp-gallery").on("click",function(a){if("slide "==a.target.className||"close"==a.target.className||"slide"==a.target.className){var b=$("#links").children(".gallery-hide").length;$("#links").children(".gallery-hide").slice(1,b).css("display","none")}}),$(".ace-content-column p,.ace-content-column ul,.ace-content-column li.column p").removeAttr("style");var U=$(".aceitem_page .col-md-3");U.before(U.find(".case-studies-illustrations")),U.before(U.find(".sidebar_files"));var V=$(".use-cases-listing tbody tr");V.each(function(){var a=$(this),b=a.find("td:last-child").text();a.find("td:first-child").append($('<span class="use-case-tooltip"/>')),a.find(".use-case-tooltip").text(b)}),$(".use-cases-listing tr td:nth-child(2)").hover(function(){$(this).siblings().find(".use-case-tooltip").css("display","block")},function(){$(this).siblings().find(".use-case-tooltip").css("display","none")}),$("input[type='checkbox']").on("click",function(){var a=$(this).parents(".subnationals-checkbox-ul");a[0]&&(this.checked?$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).show()}.bind(this)):$("#subnationals").children().each(function(a,b){var c=$(this).val();b.text.indexOf(c)!==-1&&$(b).hide()}.bind(this)))});var W=$(".subsection-tools-urban-adaptation-climatic-threats").length>0;W&&h.addClass("fullwidth");var X=$(".tile");X.each(function(){$this=$(this),0===$this.children().length&&$this.hide()}),$("a").each(function(){var a=$(this),b=0==a.parents(".header").length;if(b){var c=new RegExp("/"+window.location.host+"/");c.test(this.href)||a.attr("target","_blank")}});var Y=$("#uast-image-map").children("area");Y.each(function(){this.href=this.href.replace("/tools","/knowledge/tools")}),$(".acecontent_filtering_tile select").on("change",function(a){$(this).parents("form").submit()}),$(".sub-menu-link").each(function(){var a=$(this);a.attr("href")||(a.hover(function(){a.css("color","#3a3a3a")}),a.css("color","#3a3a3a"))}),window.require&&window.requirejs&&(requirejs.config({paths:{qtip2:"//cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/jquery.qtip.min"}}),requirejs(["qtip2"],g))});