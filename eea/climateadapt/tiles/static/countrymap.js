var _selectedMapSection = null;
var _mapTooltip = null;
// var countrySettings = {};   // country settings extracted from ajax json

$(document).ready(function () {

  // initialize the countries map
  var cpath = '++theme++climateadaptv2/static/countries/euro-countries.geojson';
  var fpath = '++theme++climateadaptv2/static/countries/countries.tsv';

  var $sw = $('.svg-header-wrapper');
  var $load = $('<div class="map-loader">' +
  '<div class="loading-spinner"></div>' +
  '<span class="loading-text">Loading map ...</span></div>');
  $sw.append($load);

  d3.json(cpath, function (world) {
    d3.json('@@mapSingleCountrySettings', function (metadata) {
      d3.tsv(fpath, function (flags) {
        initmap(metadata, world, flags);
      });
    });
  });

});


function initmap(metadata, world, flags) {
  // countrySettings = metadata[0];
  var sections = metadata[1];

  var world = world.features;
  setCountryFlags(world, flags);

  var focusCountry = metadata.focusCountry;

  function drawMap(width) {
    drawCountries(world, focusCountry);
  }

  // fire resize event after the browser window resizing it's completed
  var resizeTimer;
  $(window).resize(function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(doneResizing, 500);
  });

  var width = $('.svg-header-wrapper svg').width();
  function doneResizing() {
    drawMap(width);
  }

  drawMap(width);

  $('.map-loader').fadeOut(600);
}

function renderGraticule(container, klass, steps, pathTransformer) {
  container     // draw primary graticule lines
    .append('g')
    .attr('class', klass)
    .selectAll('path')
    .data(d3.geoGraticule().step(steps).lines())
    .enter()
    .append('path')
    .attr('d', pathTransformer)
    ;
}

function getCountryClass(country, countries) {
  var k = 'country-outline';
  var available = countries.names.indexOf(country.properties.SHRT_ENGL) !== -1;
  if (available) k += ' country-available';

  return k;
}

function renderCountry(map, country, path, countries, x, y) {

  var cprectid = makeid();    // unique id for this map drawing
  var klass = getCountryClass(country, countries);
  var cId = 'c-' + cprectid + '-' + country.properties.id;
  var cpId = 'cp-' + cprectid + '-' + country.properties.id;

  var available = countries.names.indexOf(country.properties.SHRT_ENGL) !== -1;

  var parent = map
    .append('g')
    .attr('class', klass)
    ;

  parent       // define clipping path for this country
    .append('defs')
    .append('clipPath')
    .attr('id', cpId)
    .append('path')
    .attr('d', path(country))
    .attr('x', x)
    .attr('y', y)
    ;

  var outline = parent       // this is the country fill and outline
    .append('path')
    .attr('id', cId)
    .attr('x', x)
    .attr('y', y)
    .attr('d', path(country))
    ;

  if (available) {
    var bbox = outline.node().getBBox();
    renderCountryFlag(parent, country, bbox, cpId);
  }
}

function renderCountryFlag(parent, country, bbox, cpId) {
  var flag = parent
    .append('image')
    .attr('class', 'country-flag')
    .attr('href', country.url)
    .attr("preserveAspectRatio", "none")
    .attr('opacity', '1')
    .attr('clip-path', 'url(#' + cpId + ')')
    .attr('x', bbox.x)
    .attr('y', bbox.y)
    .attr('height', bbox.height)
    .attr('width', bbox.width)
    .on('mouseover', function (e) {
      $('.country-flag').css('cursor', 'unset');
    })
    ;
  // passThruEvents(flag);
  return flag;
}


function renderCountriesBox(opts) {

  var coords = opts.coordinates;
  var countries = opts.focusCountries;

  var svg = opts.svg;
  var world = opts.world;
  var zoom = opts.zoom;
  var cprectid = makeid();    // unique id for this map drawing

  var globalMapProjection = d3.geoAzimuthalEqualArea();

  globalMapProjection
    .scale(1)
    .translate([0, 0])
    ;

  // the path transformer
  var path = d3.geoPath().projection(globalMapProjection);

  var x = coords.x;
  var y = coords.y;
  var width = coords.width;
  var height = coords.height;
  // var extent = [[x + 20, y + 20], [x + coords.width - 20 , y + coords.height - 20]];
  // console.log('fitting extent', extent);
  // globalMapProjection.fitExtent(extent, countries.feature);

  var b = path.bounds(countries.feature);
  var cwRatio = (b[1][0] - b[0][0]) / width;    // bounds to width ratio
  var chRatio = (b[1][1] - b[0][1]) / height;   // bounds to height ratio
  var s = zoom / Math.max(cwRatio, chRatio);
  var t = [
    (width - s * (b[1][0] + b[0][0])) / 2 + x,
    (height - s * (b[0][1] + b[1][1])) / 2 + y
  ];

  globalMapProjection.scale(s).translate(t);

  svg
    .append('defs')    // rectangular clipping path for the whole drawn map
    .append('clipPath')
    .attr('id', cprectid)
    .append('rect')
    .attr('x', x)
    .attr('y', y)
    .attr('height', height)
    .attr('width', width)
    ;

  var map = svg   // the map will be drawn in this group
    .append('g')
    .attr('clip-path', 'url(#' + cprectid + ')')
    ;

  map     // the world sphere, acts as ocean
    .append("path")
    .datum(
    {
      type: "Sphere"
    }
    )
    .attr("class", "sphere")
    .attr("d", path)
    ;

  renderGraticule(map, 'graticule', [20, 10], path);
  renderGraticule(map, 'semi-graticule', [5, 5], path);

  world.forEach(function (country) {
    renderCountry(map, country, path, countries, x, y);
  });

  return path;
}


function drawCountries(world, focusCountry) {
  var svg = d3
    .select("body")
    .select(".svg-map-container svg")
    ;
  svg.selectAll("*").remove();
  var svgw = $(window).width();
  svg.style('width', '100%');

  // var focusCountryNames = Object.keys(countrySettings);
  var focusCountryNames = [focusCountry];

  var focusCountriesFeature = filterCountriesByNames(
    world, focusCountryNames
  );

  var width = Math.round($(svg.node()).width());
  var height = Math.round($(svg.node()).height());

  var opts = {
    'world': world,
    'svg': svg,
    'coordinates': {
      'x': 0,
      'y': 0,
      'width': width,
      'height': height
    },
    'focusCountries': {
      'names': focusCountryNames,
      'feature': focusCountriesFeature
    },
    'zoom': 0.8
  }
  renderCountriesBox(opts);
}


function filterCountriesByNames(countries, filterIds) {
  var features = {
    type: 'FeatureCollection',
    features: []
  };
  countries.forEach(function (c) {
    if (filterIds.indexOf(c.properties.SHRT_ENGL) === -1) {
      return;
    }
    features.features.push(c);
  });
  return features;
}


function setCountryFlags(countries, flags) {
  // annotates each country with its own flag property
  countries.forEach(function (c) {
    var name = c.properties.SHRT_ENGL;
    if (!name) {
      // console.log('No flag for', c.properties);
      return;
    }
    var cname = name.replace(' ', '_');
    flags.forEach(function (f) {
      if (f.url.indexOf(cname) > -1) {
        c.url = f.url;
      }
    });
  });
}


function makeid() {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

  for (var i = 0; i < 5; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}


function travelToOppositeMutator(start, viewport, delta) {
  // point: the point we want to mutate
  // start: starting point (the initial anchor point)
  // viewport: array of width, height
  // delta: array of dimensions to travel

  var center = [viewport[0] / 2, viewport[1] / 2];

  var dirx = start[0] > center[0] ? -1 : 1;
  var diry = start[1] > center[1] ? -1 : 1;

  return function (point) {
    var res = [
      point[0] + delta[0] * dirx,
      point[1] + delta[1] * diry
    ];
    return res;
  };
}
