$(document).ready(function() {

  // HOMEPAGE: initialize slick slider
  if ($('.slider').slick) {
    $('.slider').slick({
      infinite: true,
      speed: 500,
      fade: true,
      slidesToShow: 1,
      dots:  true,
      autoplay: true,
      autoplaySpeed: 4000
    });
  }

  // HOMEPAGE: move slick slider dots to slider caption area
  // $(".slick-dots").prependTo(".slider-bottom-caption");

  // HOMEPAGE: align slider caption and slider arrows to the main content area
  function getPageContainerPadding() {
    var cw = $(".content-container").width();
    var ww = $(window).width();
    var cwRight = (ww - cw) / 2;
    return cwRight;
  }

  $('.slider .slick-prev').css('left', function() {
    return getPageContainerPadding() +  'px';
  });
  $('.slider .slick-next').css('left', function() {
    return getPageContainerPadding() + 45 +  'px';
  });
  $('.slider-caption').css('right', function() {
    return getPageContainerPadding() +  'px';
  });

  // fire resize event after the browser window resizing it's completed
  var resizeTimer;
  $(window).resize(function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(doneResizing, 500);
  });

  function doneResizing() {
    $('.slider .slick-prev').css('left', function() {
      return getPageContainerPadding() +  'px';
    });
    $('.slider .slick-next').css('left', function() {
      return getPageContainerPadding() + 45 +  'px';
    });
    $('.slider-caption').css('right', function() {
      return getPageContainerPadding() +  'px';
    });
  }

  // HOMEPAGE: Tabs functionality
  $('ul.nav-tabs a').click(function(e) {
    $(this).tab('show');
    e.preventDefault();
  });

  // HOMEPAGE: Dynamic area:
  // on click center tab items on small screen sizes
  $('.main-nav-tabs li a').click(function() {
    var $parent = $(this).parent();
    centerTabItem($parent, '.main-tab-heading .main-nav-tabs');
  });

  function centerTabItem(target, outer) {
    var outer = $(outer);
    var target = $(target);
    var outerW = outer.width();
    var targetW = target.outerWidth(true);
    var targetIn = target.index();
    var q = 0;
    var centerElement = outer.find('li');

    for (var i = 0; i < targetIn; i++) {
      q += $(centerElement[i]).outerWidth(true);
    }

    outer.animate({
      scrollLeft: Math.max(0, q - (outerW - targetW) / 2)
    }, 500);
  }

  // HOMEPAGE: Dynamic area - Getting started:
  // On button hover toggle class on the bubble section
  $('.action-btn').each(function() {
    $(this).hover(function() {
      if ($(this).hasClass('regional-btn')) {
        $(this).siblings('.action-bubble').toggleClass('regional-bubble');
      }
      if ($(this).hasClass('transnational-btn')) {
        $(this).siblings('.action-bubble').toggleClass('transnational-bubble');
      }
      if ($(this).hasClass('national-btn')) {
        $(this).siblings('.action-bubble').toggleClass('national-bubble');
      }
    })
  });

  // HOMEPAGE: Dynamic area - Adaptation support tool:
  // Highlight steps on hover
  $('.dynamic-area .ast-step-wrapper').hover(function() {
    $(this).children('.ast-circle').css({
      'background-color': '#FFD554',
      'border': '2px solid #F2C94C',
      'transform': 'scale(1.08)',
      'color': '#4F4F4F'
    });
    $(this).children('.step-text').css({
      'background-color': '#FFD554',
      'transform': 'scale(1.08)'
    });

    }, function() {
    $(this).children('.ast-circle').css({
      'background-color': '#B8D42F',
      'border': '2px solid #A5BF26',
      'transform': 'scale(1)',
      'color': '#fff'
    });
    $(this).children('.step-text').css({
      'background-color': '#f5f5f5',
      'transform': 'scale(1)'
    });
  });

  // HOMEPAGE: Dynamic area - EU Sector policies:
  // Sub-tab section close functionality
  $(".close-tab-pane").click(function() {
    var $contentParent = $(this).closest('.policies-tab-content');
    var $mainParent = $(this).closest('.sub-tab-section');
    $mainParent.find('.action-flex-item').removeClass('active');
    $contentParent.removeClass('active');
  });

  // Mobile menu button on click event
  $('.mobile-menu i').click(function() {
    $('body').toggleClass('no-ovf');
    $(this).toggleClass('fa-bars fa-times');
    $('.header').toggleClass('mobile-header');
    $('.header .main-nav, .top-menu-content').toggleClass('nav-toggle');

    return false;
  });

  // Mobile - show submenus on click
  $('.angle-down-icon').click(function() {
    $(this).parent().siblings('.sub-menu-wrapper').toggle();
  });

  // Top menu login
  $('#user-name').click(function(e) {
    e.preventDefault();
  });

  // Navigation menu: align sub-menu to the right
  // if overflows the main navigation menu
  var mainMenuWidth = $('.main-nav').width();

  $('.main-nav li').mouseenter(function() {
    var subMenuWidth = $(this).children('.sub-menu-wrapper').width();
    if ($(this).find('.sub-menu-wrapper').length > 0) {
      var subMenuLeft = $(this).children('.sub-menu-wrapper').offset().left;
    }

    if (mainMenuWidth - (subMenuWidth + subMenuLeft) < 0) {
      $(this).children('.sub-menu-wrapper').css({
        'right': 0,
        'left': 'auto'
      });
    }
  });

  // divide the sub-menu in 2 columns if 'sub-sub-menu' exist
  var navigationItem = $('.main-nav-item');
  navigationItem.each(function() {
    if ($(this).find('.sub-sub-menu-wrapper').length > 0) {
      $(this).find('.sub-menu-wrapper').css('column-count', '2');
    }
  });

  // add primary button class to share your information
  $('.share-your-info-ace-button button').addClass('standard-button primary-button');

  // add btn class to download as pdf
  $("#document-action-download_pdf").find('a').addClass('standard-button secondary-button');
  $("#login-form .formControls input").addClass('standard-button secondary-button');

  // EU POLICY PAGES AND TRANSNATIONAL REGIONS:
  // add a specific class for policy pages and transnational regions
  var currentLocation = window.location.pathname;
  var lastPathName;
  var parts = currentLocation.split("/");

  if (parts[parts.length-1].length == 0) {
    lastPathName = parts[parts.length - 2];
  } else {
    lastPathName = parts[parts.length - 1];
  }

  var policyClass = 'subsection-sector-policies-' + lastPathName;
  var regionClass = 'subsection-transnational-regions-' + lastPathName;
  var countryClass = 'subsection-countries-' + lastPathName;

  var bodyClassList = $('body').attr('class').split(/\s+/);
  $.each(bodyClassList, function(index, item) {
    if (item === policyClass) {
      $('body').addClass('eu-policy-page');
    }
    if (item === regionClass) {
      $('body').addClass('region-page');
    }
    if (item === countryClass) {
      $('body').addClass('country-page');
    }
  });

  var isPolicyPage = $('.eu-policy-page').length > 0;
  var isRegionPage = $('.region-page').length > 0;
  var isCountryPage = $('.country-page').length > 0;

  if (isPolicyPage || isRegionPage) {
    $('.region-page .column.col-md-2').removeClass('col-md-2').addClass('col-md-3');
    $('.region-page .column.col-md-10').removeClass('col-md-10').addClass('col-md-9');
    $('.region-page #content-core .row').prepend($('.column.col-md-9'));

    $('.column.col-md-9').children().wrapAll('<div class="content-column"/>');
    $('.column.col-md-3').children().wrapAll('<div class="content-sidebar"/>');

    $('.content-column').find('img').closest('.tile-content').addClass('main-tile-content');
    $('.content-column').children('.col-md-4').wrapAll('<div class="row"/>');

    // move pdf button and 'last modified' viewlet to the main content area
    $('#document-action-download_pdf').parent().appendTo(".content-column");
    $('.content-column').prepend($('#viewlet-below-content-title'));
  }

  $('.region-page #trans-region-select').siblings('div').addClass('region-countries');

  var regionsTitle = $('.region-countries').children('strong');
  regionsTitle.each(function() {
    $(this).replaceWith($('<h5>' + this.innerHTML + '</h5>'));
  });

  if (isPolicyPage) {
    var policySubTitles = $('.read_more_second').children('h2');

    policySubTitles.each(function() {
      $(this).replaceWith($('<p><strong>' + this.innerHTML + '</strong><p>'));
    });

    $('.main-tile-content').prepend('<div class="flex-wrapper"/>');
    $('.flex-wrapper').append([
      $('.main-tile-content img'),
      $('.read_more_first')
    ]);

    var policyTitle = $('.main-tile-content').children('h2');
    $('.main-tile-content').prepend([
      policyTitle,
      $('.main-tile-content').children().find('h2')
    ]);

    // Eu sector policy factsheet
    var factsheetIMG = $('.content-sidebar .image-inline').parent();
    var factheetCategory = $('.main-tile-content h2').text();

    factsheetIMG.html(function(i,h) {
      return h.replace(/&nbsp;/g,'');
    });

    $('.column.col-md-3').prepend(factsheetIMG);
    $('.column.col-md-3 .image-inline').parent().append(
    '<div class="factsheet-pdf">' +
    '<i class="fa fa-angle-double-right"></i>' +
    '<div class="factsheet-title">Factsheet on <span>' +
    factheetCategory + '</span></div></div>');
    $('.column.col-md-3 .image-inline').hide();
  }

  var isBalticSubpage = $('.subsection-transnational-regions-baltic-sea-region-adaptation').length > 0;
  var isCarpathianSubpage = $('.subsection-transnational-regions-carpathian-mountains').length > 0;

  if (isBalticSubpage || isCarpathianSubpage) {
    $('body').addClass('region-subpage');
    $('#content-core .column.col-md-3').remove();
    $('#content-core .column.col-md-9').removeClass('col-md-9');

    $('.tile-content').addClass('clearfix');

    // add active class on current page sub-navigation item
    $(function() {
      var current = window.location.pathname;
      var current = current.substring(current.lastIndexOf("/") + 1, current.length);
      $('.cover-section_nav-tile a').each(function() {
        var getURL = $(this).attr('href');
        var getURL = getURL.substring(getURL.lastIndexOf("/") + 1, getURL.length);
        if(getURL.indexOf(current) !== -1) {
          $(this).addClass('active-nav');
        }
      })
    })
  }

  if (isCountryPage) {
    $('.column.col-md-10').parents('.row').removeClass('row').addClass('country-wrapper');
    $('.column.col-md-2').removeClass('col-md-2');
    $('.column.col-md-10').removeClass('col-md-10');
    $('.sweet-tabs').attr('id', 'country-tab');

    $('.country-wrapper .column:first-child').addClass('country-header-map');
    $('.country-wrapper .column:nth-child(2)').addClass('country-content');

    $('.country-select-tile').parent().addClass('countries-dropdown');
    $('.country-select-tile img').remove();

    $('.country-header-map').append($('<div class="country-map">'));
    $('.country-content .last-update-tile').addClass('clearfix').prependTo('.tab-pane');

    $('#document-action-download_pdf').parent().appendTo(".tab-pane");

    // custom country dropdown functionality
    $('.dd-country-title .options li').on('click', function() {
      $('.dd-country-title .selected').html($(this).text());
      $('.dd-country-title .selected-inp').val($(this).data('value')).trigger('change');
      $('.dd-country-title .options').removeClass('show');
    });

    $('.dd-title-wrapper').on('click', function(e) {
      $('.dd-country-title .options').fadeToggle().toggleClass('show');
      $('.dd-country-title i').toggleClass('fa fa-angle-up fa fa-angle-down');
      e.stopPropagation()
    });

    $('.dd-country-title .selected-inp').on('change', function(ev) {
      var url = ev.target.value;
      var country = $(".dd-country-title li[data-value='" + url + "']").text();

      if (country.length) {
        document.location = '/countries/' + country.toLowerCase();
      }
    });

    $.fn.resizeselectList = function(settings) {
      return this.each(function() {
        $(this).change(function() {
          var $this = $(this);
          var $selected = $this.parents().find('.dd-country-title .selected');
          var text = $selected.text();
          console.log(text);

          var $test = $("<span class='xx'/>").html(text).css({
            "font-size": $selected.css("font-size"),
            "font-weight": $selected.css("font-weight"),
            "visibility": "hidden"
          });


          $test.appendTo($this.parent());
          var width = $test.width();
          $test.remove();

          $this.width(width + 45);
        }).change();
      });
    };
    $(".resizeselect-list").resizeselectList();
  }

  // ADAPTATION SUPPORT TOOL
  var isASTPage = $('.subsection-tools-adaptation-support-tool').length > 0;
  $('.lfc-single-image').remove(); // remove existing AST image

  if (isASTPage) {
    $('.col-md-8').children('.tile:nth-child(2)').addClass('tile-wrapper');

    var titleAST = $('.tile-content').children('h1');
    titleAST.each(function() {
      $('<h2>' + $(this).html() + '</h2>').replaceAll(this);
    });
  }

  $('.ast-map .ast-circle').hover(function() {
    $(this).siblings(".step-text").css('display', 'block');
  }, function() {
    $(this).siblings(".step-text").css('display', 'none');
  });

  var currentStep = $('.ast-title-step').text();
  var circleStep = $('.ast-circle');

  if (currentStep == 0) {
    $('.ast-title-step').remove();
  }

  // highlight the current step
  circleStep.each(function() {
    if ($(this).text() === currentStep) {
      $(this).css({
        'background-color': '#FFD554',
        'border': '2px solid #F2C94C',
        'color': '#4F4F4F'
      });
    }
  });

  /*
  * For mobile: fix table styling issues
  *
  *
  * */
  function resizehandlerforContentTables(ev){
      if (window.matchMedia("(max-width: 480px)").matches) {
          $.each( $(".content-container table"),function (indx, item) {
              if($(item).parent().prop("tagName") !== "DIV" ){
                  $(item).wrapAll('<div style="overflow-x: auto;width: 86vw; "></div>');
              } else {
                  $(item).parent().css({
                      "overflow-x": "auto",
                      "width" : "86vw"
                  });
              }
          });
      }
  }

  var isCities = $(".subsection-cities.subsection-cities-index_html").length > 0;

  /*
  * added font awesome arrows for menu item section
  * */
  function DoubleAngleListStyle(){
    $.each($("#content .cover-richtext-tile.tile-content:not(aceitem-urban-menu-tile) ul > li"), function (idx, item) {
      var $item = $(item);
      var $parent = $item.parent();
      var $parent_class = $parent.attr('class');

      if( $parent_class!== undefined && !$parent_class.indexOf("menu-urban-sub")
          && !$parent_class.indexOf("menu-urban")
          && !$parent_class.indexOf("aceitem-search-tile-listing")
          && $parent.find("ul").length === 0
          && $item.find("a").length > 0
          && !$item.hasClass("fa")
      ){
        $item.addClass("fa fa-angle-double-right");
      }
    });
  }

  /*
  *  Adaptation options
  * - http://climate-local.com/cca/knowledge/adaptation-information/adaptation-measures
  * - remove double list decoration
  * */
  function AdaptationOptions(){
    $(".subsection-tools-general.subsection-tools-general-index_html ul li").removeClass("fa").removeClass("fa-angle-double-right");

    $(".subsection-adaptation-information-climate-services.subsection-adaptation-information-climate-services-climate-services " +
        ".tile-content ul li.fa.fa-angle-double-right")
        .removeClass("fa").removeClass("fa-angle-double-right");

    if( $(".subsection-adaptation-information-adaptation-measures-index_html .aceitem-search-tile").length > 0 ||
        $(".subsection-adaptation-information-climate-services.subsection-adaptation-information-climate-services-climate-services .aceitem-search-tile").length > 0 )
    {
        fixSidebarAndColumns();
    }

    if($(".subsection-adaptation-information-adaptation-measures-index_html").length > 0){
        $.each( $(".aceitem-search-tile li ul li"), function(idx, item){
            var ia = $(item).find("a").prop('outerHTML');
            $(item).replaceWith('<li class="fa fa-angle-double-right">'+ ia +'</li>');
        });
    }
  }

  /*
  *
  * Cities fixes
  * - Page: http://climate-local.com/cca/countries-regions/cities
  * - fixing HTML structure
    * */
  function CitiesFixes(){
    /*
    * adding to first column .content-column and moving siblings
    * */
    if( isCities){

        var divs = $("#content-core .column.col-md-9 > div");
        $("#content-core .column.col-md-9").prepend('<div class="content-column"></div>');
        $("#content-core .column.col-md-9 .content-column").append(divs);

        // moving download button to .content-column
        $(" #content-core .content-column").append( $(".subsection-cities-index_html #document-action-download_pdf"));
        $("#document-action-download_pdf").css({
            "display": "block",
            "clear" : "both",
            "float" : "none"
        });

        $("#document-action-download_pdf").wrap("<ul></ul>");

        // adding .row to .tile-default
        var sib = $("#content-core .column.col-md-9 .tile-default").siblings();
        $("#content-core div.column.col-md-9 .content-column").append('<div class="row"></div>');
        $("#content-core div.column.col-md-9 .content-column > .row").append(sib);
    }

  }

  function SidebarFixes() {
      /* Sidebar fixes
      * - http://climate-local.com/cca/countries-regions/cities
      * - http://climate-local.com/cca/knowledge/adaptation-information/vulnerabilities-and-risks
      * - http://climate-local.com/cca/knowledge/adaptation-information/adaptation-measures
      * - http://climate-local.com/cca/knowledge/adaptation-information/observations-and-scenarios
      * */
    var sels = [
        ".subsection-cities.subsection-cities-index_html .aceitem-search-tile",
        ".subsection-adaptation-information-vulnerabilities-and-risks-index_html .aceitem-search-tile",
        ".subsection-adaptation-information-adaptation-measures-index_html .aceitem-search-tile",
        ".subsection-adaptation-information-observations-and-scenarios-index_html .aceitem-search-tile"
    ];

    // adding .content-sidebar to .aceitem-search-tile parent
    $.each(sels , function (ix, sel){
      $(sel).parent().parent().prepend('<div class="content-sidebar"></div>');
      var sib = $(sel).parent().parent().find(".content-sidebar").siblings();

      $(sel).parent().parent().find(".content-sidebar").append(sib);
    });
  }

  /*
  * Observations and Scenarios:
  * - http://climate-local.com/cca/knowledge/adaptation-information/observations-and-scenarios
  * */
  function ObservationsAndScenarios(){
    if( $(".subsection-adaptation-information-observations-and-scenarios-index_html .aceitem-search-tile").length > 0 ){
      fixSidebarAndColumns();
    }
  }

  /*
  * Vulnerabilities and fixes
  * - http://climate-local.com/cca/knowledge/adaptation-information/vulnerabilities-and-risks
  * */
  function VulnerabilitiesAndRisksFixes(){
      if( $(".subsection-adaptation-information-vulnerabilities-and-risks-index_html .aceitem-search-tile").length > 0 ){
          fixSidebarAndColumns();
      }
  }

  function fixSidebarAndColumns(){
    // fix background of #content
    $("#content").css({
        "background-color" :"transparent",
        "padding" : 0,
        "margin" : 0,
        "border" : 0
    });

    // add content-column to first column
    $($("#content-core .column")[0]).prepend('<div class="content-column"></div>');

    $("#content-core .content-column").append($("#content-core .content-column").siblings());

    // add "clearfix" div to fix height issue
    $("#content-core .content-column").append('<div class="clearfix"></div>');

    // move download button to content-column
    $("#content-core .content-column").append( $(" #document-action-download_pdf"));

  }

  function addingLinetoMoreThan1Tile(){
    $.each( $(".content-column"), function (idx, col) {
        if( $(col).find(".tile").length > 1){
          $(col).find(".tile-default").css({
             "padding-bottom" : "2rem",
             "border-bottom" : "1px solid #eee",
              "margin-bottom" : "2.5rem"

          });
        }
    } );

  }

  function StylingFixes(){
    DoubleAngleListStyle();
    AdaptationOptions();
    CitiesFixes();
    VulnerabilitiesAndRisksFixes();
    ObservationsAndScenarios();
    SidebarFixes();
    addingLinetoMoreThan1Tile();
  }

  resizehandlerforContentTables();
  $( window ).resize(resizehandlerforContentTables);

  StylingFixes();

});
