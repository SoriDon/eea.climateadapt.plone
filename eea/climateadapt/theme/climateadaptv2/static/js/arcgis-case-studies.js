window.requirejs.config({baseUrl:"https://js.arcgis.com/4.18/"}),window.requirejs(["esri/Map","esri/layers/GeoJSONLayer","esri/views/MapView","esri/geometry/Point"],function(e,t,s,a){let n=new t({url:"./case-studies-map.arcgis.json",featureReduction:{type:"cluster",clusterRadius:"60px",labelPlacement:"center-center",clusterMinSize:"20px",clusterMaxSize:"40px",popupEnabled:!0,popupTemplate:{title:"hello4",content:function e(t){t.graphic.visible=!1;var s=t.graphic.geometry;return $(".esri-component.esri-popup").css("display","none"),r.goTo({center:[s.longitude,s.latitude],animation:!0}),zoomValue=Math.min(r.zoom+1,12),r.zoom=zoomValue,"<div id='popup-cluster'><div>"}},labelingInfo:[{labelExpressionInfo:{expression:"Text($feature.cluster_count, '#,###')"},symbol:{type:"text",color:"#ffffff",borderLineSize:0,font:{weight:"bold",family:"Noto Sans",size:"16px"}},labelPlacement:"center-center"}]},renderer:{type:"simple",symbol:{type:"simple-marker",size:8,color:"#005c96",outline:{width:0}},visualVariables:[{type:"color",field:"origin_adaptecca",stops:[{value:10,color:"#00FFFF"},{value:20,color:"#005c96"}]}]},popupTemplate:{title:"<strong>{title}</strong> <a href='{url}'>open DB</a>",outFields:["*"],content:function e(t){var s=t.graphic.geometry;zoomAdjustment=[8,7,4,2,1,.9,.7,.2,.1,.05,.04,.02],(viewZoom=parseInt(r.zoom,10))&&zoomAdjustment.length>viewZoom?r.goTo({center:[s.longitude,s.latitude-zoomAdjustment[viewZoom-1]]}):r.goTo({center:[s.longitude,s.latitude]});var a=document.createElement("div"),n=t.graphic.attributes.sectors_str,o=t.graphic.attributes.impacts_str,c=t.graphic.attributes.adaptation_options_links;return t.graphic.attributes.image.length&&(a.innerHTML+='<span style="background-color:#ddd;display:block;margin-bottom:10px;"><center><img style="max-height:133px;" src="'+t.graphic.attributes.image+'" /></center></span>'),n.length&&(a.innerHTML+='<p style="font-size:13px;margin-bottom:10px;""><span style="color:#069;">Adaptation sectors:</span> '+n.split(",").join(", ")+"</p>"),a.innerHTML+='<p style="font-size:13px;margin-bottom:10px;""><span style="color:#069;">Climate impacts:</span> '+o+"</p>",c.length&&(a.innerHTML+='<p class="cs_adaptation_casestudies" style="font-size:13px;margin-bottom:5px;""><span style="color:#069;">Adaptation options:</span> '+c.split("<>").join("; ")+"</p>"),$(".esri-component.esri-popup").css("display","block"),a}}}),o=new e({basemap:"gray-vector",layers:[n]}),r=new s({container:"arcgisDiv",center:[2,53],zoom:3,map:o,popup:{actions:[],alignment:"bottom-center",dockOptions:{buttonEnabled:!1}}});window.iugMapView=r,window.iugPoint=a,r.filter={where:"portal_type 'casestudy'"},r.whenLayerView(n).then(function(e){window.mapview=e,updateItems()})});var changeSkipClicks=!1;function pageLoadMap(){if(sectorsData=(params=new URLSearchParams(window.location.search)).get("sectors"))for((sectors=sectorsData.split(",")).length&&($(".cs_filter_sector_div h4").click(),changeSkipClicks=!0),i=0;i<sectors.length;i++)$('.cs_filter_sector_div input[value="'+sectors[i]+'"]').click()}function buttonReset(){$(".case-study-row .case-study-div input:checked").length>0?$(".case-study-row .case-study-div a.reset").show():$(".case-study-row .case-study-div a.reset").hide()}function filterDisplayMode(e){$(e).hasClass("active")?$(e).removeClass("active").parent().find("p").hide():$(e).addClass("active").parent().find("p").show()}function updateItems(e){let t=[],s=[],a=[],n=[],o=[];t.push("portal_type LIKE 'casestudy'");let r=$("#arcgis_case_study_form input[name='impacts']:checked");for(index=0;index<r.length;index++)s.push("impacts LIKE '%"+r[index].getAttribute("value")+"%'");s.length&&t.push("("+s.join(" OR ")+")");let c=$("#arcgis_case_study_form input[name='sectors']:checked");for(index=0;index<c.length;index++)a.push("sectors LIKE '%"+c[index].getAttribute("value")+"%'");a.length&&t.push("("+a.join(" OR ")+")");let p=$("#arcgis_case_study_form input[name='ipccs']:checked");for(index=0;index<p.length;index++)n.push("ipccs LIKE '%"+p[index].getAttribute("value")+"%'");n.length&&t.push("("+n.join(" OR ")+")");let l=$("#arcgis_case_study_form input[name='ktms']:checked");for(index=0;index<l.length;index++)o.push("ktms LIKE '%"+l[index].getAttribute("value")+"%'");o.length&&t.push("("+o.join(" OR ")+")"),window.mapview.filter={where:t.join(" AND ")}}$(document).ready(function(){for($('#arcgis_case_study_form input[name="impacts"], #arcgis_case_study_form input[name="sectors"], #arcgis_case_study_form input[name="ktms"]').change(function(){changeSkipClicks||(buttonReset(),updateItems()),changeSkipClicks=!1}),$("#arcgis_case_study_form h4").click(function(){filterDisplayMode(this)}),$(".case-study-row .case-study-div a.reset").click(function(){return $(".case-study-row .case-study-div input:checked").click(),$(".case-study-row .case-study-div h4").removeClass("active"),$(".case-study-row .case-study-div form p").hide(),!1}),buttonReset(),elements=$("#arcgis_case_study_form h4"),i=0;i<elements.length;i++);pageLoadMap()});