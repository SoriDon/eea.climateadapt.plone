function filterDisplayMode(a){console.log("aici",a),$(a).hasClass("active")?$(a).removeClass("active").parent().find("p").hide():$(a).addClass("active").parent().find("p").show()}function updateItems(a){const b=[],c=[],d=[],e=[];b.push("portal_type LIKE 'casestudy'");const f=$("#arcgis_case_study_form input[name='impacts']:checked");for(index=0;index<f.length;index++)c.push("impacts LIKE '%"+f[index].getAttribute("value")+"%'");c.length&&b.push("("+c.join(" OR ")+")");const g=$("#arcgis_case_study_form input[name='sectors']:checked");for(index=0;index<g.length;index++)d.push("sectors LIKE '%"+g[index].getAttribute("value")+"%'");d.length&&b.push("("+d.join(" OR ")+")");const h=$("#arcgis_case_study_form input[name='ipccs']:checked");for(index=0;index<h.length;index++)e.push("ipccs LIKE '%"+h[index].getAttribute("value")+"%'");e.length&&b.push("("+e.join(" OR ")+")"),window.mapview.filter={where:b.join(" AND ")}}window.requirejs.config({baseUrl:"https://js.arcgis.com/4.18/"}),window.requirejs(["esri/Map","esri/layers/GeoJSONLayer","esri/views/MapView","esri/geometry/Point"],function(a,b,c,d){function e(a){var b=a.graphic.geometry;zoomAdjustment=[8,7,4,2,1,.9,.7,.2,.1,.05,.04,.02],k.zoom&&zoomAdjustment.length>k.zoom?k.goTo({center:[b.longitude,b.latitude-zoomAdjustment[k.zoom-1]]}):k.goTo({center:[b.longitude,b.latitude]});var c=document.createElement("div"),d=a.graphic.attributes.sectors_str,e=a.graphic.attributes.impacts_str,f=a.graphic.attributes.adaptation_options_links;return a.graphic.attributes.image.length&&(c.innerHTML+='<span style="background-color:#ddd;display:block;margin-bottom:10px;"><center><img style="max-height:133px;" src="'+a.graphic.attributes.image+'" /></center></span>'),d.length&&(c.innerHTML+='<p style="font-size:12px;margin-bottom:10px;""><span style="color:#069;">Adaptation sectors:</span> '+d.split(",").join(", ")+"</p>"),c.innerHTML+='<p style="font-size:12px;margin-bottom:10px;""><span style="color:#069;">Climate impacts:</span> '+e+"</p>",f.length&&(c.innerHTML+='<p class="cs_adaptation_casestudies" style="font-size:12px;margin-bottom:5px;""><span style="color:#069;">Adaptation options:</span> '+f.split("<>").join("; ")+"</p>"),$(".esri-component.esri-popup").css("display","block"),c}function f(a){a.graphic.visible=!1;var b=a.graphic.geometry;return $(".esri-component.esri-popup").css("display","none"),k.goTo({center:[b.longitude,b.latitude],animation:!0}),zoomValue=Math.min(k.zoom+1,12),k.zoom=zoomValue,"<div id='popup-cluster'><div>"}const g="./case-studies-map.arcgis.json",h={title:"<strong>{title}</strong> <a href='{url}'>open DB</a>",outFields:["*"],content:e},i=new b({url:g,featureReduction:{type:"cluster",clusterRadius:"60px",labelPlacement:"center-center",clusterMinSize:"20px",clusterMaxSize:"40px",popupEnabled:!0,popupTemplate:{title:"hello4",content:f},labelingInfo:[{labelExpressionInfo:{expression:"Text($feature.cluster_count, '#,###')"},symbol:{type:"text",color:"#ffffff",borderLineSize:0,font:{weight:"bold",family:"Noto Sans",size:"16px"}},labelPlacement:"center-center"}]},renderer:{type:"simple",symbol:{type:"simple-marker",size:8,color:"#005c96",outline:{width:0}},visualVariables:[{type:"color",field:"origin_adaptecca",stops:[{value:10,color:"#3c8fdb"},{value:20,color:"#005c96"}]}]},popupTemplate:h}),j=new a({basemap:"gray-vector",layers:[i]}),k=new c({container:"arcgisDiv",center:[2,53],zoom:3,map:j,popup:{actions:[],alignment:"bottom-center",dockOptions:{buttonEnabled:!1}}});window.iugMapView=k,window.iugPoint=d,k.filter={where:"portal_type 'casestudy'"},k.whenLayerView(i).then(function(a){window.mapview=a,a.filter={where:"portal_type LIKE 'casestudy'"}})}),$(document).ready(function(){for($('#arcgis_case_study_form input[name="impacts"], #arcgis_case_study_form input[name="sectors"], #arcgis_case_study_form input[name="ipccs"]').change(function(){updateItems()}),$("#arcgis_case_study_form h4").click(function(){filterDisplayMode(this)}),elements=$("#arcgis_case_study_form h4"),i=0;i<elements.length;i++);});