//	HYPE.documents["Matchup"]

(function(){(function m(){function k(a,b,c,d){var e=!1;null==window[a]&&(null==window[b]?(window[b]=[],window[b].push(m),a=document.getElementsByTagName("head")[0],b=document.createElement("script"),e=l,false==!0&&(e=""),b.type="text/javascript",""!=d&&(b.integrity=d,b.setAttribute("crossorigin","anonymous")),b.src=e+"/"+c,a.appendChild(b)):window[b].push(m),e=!0);return e}var l="Matchup.hyperesources",f="Matchup",g="matchup_hype_container";if(false==
!1)try{for(var c=document.getElementsByTagName("script"),a=0;a<c.length;a++){var d=c[a].src,b=null!=d?d.indexOf("/matchup_hype_generated_script.js"):-1;if(-1!=b){l=d.substr(0,b);break}}}catch(p){}c=navigator.userAgent.match(/MSIE (\d+\.\d+)/);c=parseFloat(c&&c[1])||null;d=!0==(null!=window.HYPE_736F||null!=window.HYPE_dtl_736F)||true==!0||null!=c&&10>c;a=!0==d?"HYPE-736.full.min.js":"HYPE-736.thin.min.js";c=!0==d?"F":"T";d=d?"":
"";if(false==!1&&(a=k("HYPE_736"+c,"HYPE_dtl_736"+c,a,d),false==!0&&(a=a||k("HYPE_w_736","HYPE_wdtl_736","HYPE-736.waypoints.min.js","")),false==!0&&(a=a||k("Matter","HYPE_pdtl_736","HYPE-736.physics.min.js","")),a))return;d=window.HYPE.documents;if(null!=d[f]){b=1;a=f;do f=""+a+"-"+b++;while(null!=d[f]);for(var e=document.getElementsByTagName("div"),
b=!1,a=0;a<e.length;a++)if(e[a].id==g&&null==e[a].getAttribute("HYP_dn")){var b=1,h=g;do g=""+h+"-"+b++;while(null!=document.getElementById(g));e[a].id=g;b=!0;break}if(!1==b)return}b=[];b=[{name:"initFunctions",source:"function(hypeDocument, element, event) {\tconst VALUE_MAPPERS = {\n\t    \"img\": \"updateImage\",\n\t    \"color\": \"updateColor\",\n\t    \"fade\": \"fadeText\",\n\t    \"show\": \"setVisibility\",\n\t    \"playAnim\": \"playAnimation\"\n\t}\n\t\n\tfunction getMapperFunc(prefix) {\n\t    let mapperName = VALUE_MAPPERS[prefix];\n\t    let mapper = window[mapperName] || window[\"updateText\"];\n\t    return mapper;\n\t}\n\t\n\tfunction parsePayload(rawKey, value) {\n\t    [prefix, key] = rawKey.split(\":\");\n\t    mapper = getMapperFunc(prefix);\n\t    try {\n\t        console.log(prefix, key, value);\n\t        mapper(key, value);\n\t    } catch (error) {\n\t        console.error(error);\n\t    }   \n\t}\n\t\n\tfunction handlePayload(payload) {\n\t    if(payload.key.includes(\":\")) { parsePayload(payload.key, payload.value) }\n\t    else { window.updateText(payload.key, payload.value) }\n\t}\n\t\n\twindow.updateImage = function(key, src) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\thypeDocument.setElementProperty(element, \"background-image\", src)\n\t}\n\t\n\twindow.fadeOff = function(key) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\thypeDocument.setElementProperty(element, 'opacity', 0, 0.3, 'easeinout')\n\t}\n\t\n\twindow.fadeOn = function(key) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\thypeDocument.setElementProperty(element, 'opacity', 1, 0.3, 'easeinout')\n\t}\n\t\n\twindow.updateText = function(key, value) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\tif(element != null) {\n\t\t\telement.innerText = value\n\t\t}\n\t}\t\n\t\n\twindow.fadeText = function(key, value) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\tif(element.innerText === value) { return; }\n\t\tfadeOff(key)\n\t\tsetTimeout(updateText, 300, key, value)\n\t\tsetTimeout(fadeOn, 350, key, value)\n\t}\n\t\n\twindow.setVisibility = function(key, value) {\n\t\tif(value === \"1\") { fadeOn(key) }\n\t\telse { fadeOff(key) }\n\t}\n\t\n\twindow.updateColor = function(key, color) {\n\t\tlet element = hypeDocument.getElementById(key)\n\t\telement.style.backgroundColor = color\n\t}\n\t\n\twindow.update = function(payload) {\n\t\tfor([key, value] of Object.entries(JSON.parse(payload))) {\n\t\t\thandlePayload({key: key, value: value})\n\t\t}\n\t}\n\t\n\twindow.play = function() {\n\t\tif(hypeDocument.currentTimeInTimelineNamed('Main Timeline') == 0) {\n\t\t\thypeDocument.continueTimelineNamed('Main Timeline', hypeDocument.kDirectionForward, false)\n\t\t}\n\t}\n\t\n\twindow.stop = function() {\n\t\tif(hypeDocument.currentTimeInTimelineNamed('Main Timeline') > 0) {\n\t\t\thypeDocument.continueTimelineNamed('Main Timeline', hypeDocument.kDirectionForward, false)\n\t\t}\n\t}\n}",identifier:"5"},{name:"timelineSetPlaying",source:"function(hypeDocument, element, event) {\twindow.setPlaying()\n}",identifier:"137"},{name:"timelineSetStopped",source:"function(hypeDocument, element, event) {\twindow.setStopped()\n}",identifier:"138"}];e={};h={};for(a=0;a<b.length;a++)try{h[b[a].identifier]=b[a].name,e[b[a].name]=eval("(function(){return "+b[a].source+"})();")}catch(n){window.console&&window.console.log(n),e[b[a].name]=function(){}}c=new window["HYPE_736"+c](f,g,{"7":{p:1,n:"DTV%20Logo%20Small%20-%20Transparent.png",g:"135",o:true,t:"@1x"},"3":{p:1,n:"DREXEL_2x.png",g:"97",o:true,t:"@2x"},"8":{p:1,n:"DTV%20Logo%20Small%20-%20Transparent_2x.png",g:"135",o:true,t:"@2x"},"4":{p:1,n:"IBX.png",g:"121",t:"@1x"},"0":{p:1,n:"COLLEGE_OF_CHARLESTON.png",g:"91",o:true,t:"@1x"},"-2":{n:"blank.gif"},"5":{p:1,n:"CAAWhite.png",g:"131",o:true,t:"@1x"},"1":{p:1,n:"COLLEGE_OF_CHARLESTON_2x.png",g:"91",o:true,t:"@2x"},"6":{p:1,n:"CAAWhite_2x.png",g:"131",o:true,t:"@2x"},"2":{p:1,n:"DREXEL.png",g:"97",o:true,t:"@1x"},"-1":{n:"PIE.htc"}},l,["","",""],e,[{n:"Untitled Scene",o:"1",X:[0]}],
[{o:"3",dA:{a:[{p:4,h:"5"}]},p:"600px",cA:false,Y:1920,Z:1080,c:"#FFF",L:[],bY:1,d:1920,U:{},T:{kTimelineDefaultIdentifier:{q:false,z:4.05,i:"kTimelineDefaultIdentifier",n:"Main Timeline",a:[{f:"113",y:0,z:2.14,i:"b",e:234,s:423,o:"152"},{f:"q",p:2,y:0,z:3.15,i:"ActionHandler",e:{a:[{p:7,b:"kTimelineDefaultIdentifier",symbolOid:"2"}]},s:{a:[{p:7,b:"kTimelineDefaultIdentifier",symbolOid:"2"}]},o:"kTimelineDefaultIdentifier"},{f:"q",y:0.13,z:1.17,i:"b",e:63,s:253,o:"156"},{f:"q",y:0.13,z:1.17,i:"b",e:77,s:267,o:"143"},{f:"q",y:0.18,z:1.12,i:"b",e:0,s:87,o:"158"},{f:"q",y:0.18,z:1.12,i:"b",e:0,s:116,o:"144"},{f:"q",y:0.23,z:1.06,i:"b",e:179,s:273,o:"159"},{f:"q",y:0.23,z:1.07,i:"b",e:165,s:273,o:"146"},{y:1.29,i:"b",s:179,z:0,o:"159",f:"q"},{y:2,i:"b",s:63,z:0,o:"156",f:"q"},{y:2,i:"b",s:77,z:0,o:"143",f:"q"},{y:2,i:"b",s:0,z:0,o:"158",f:"q"},{y:2,i:"b",s:165,z:0,o:"146",f:"q"},{y:2,i:"b",s:0,z:0,o:"144",f:"q"},{f:"q",y:2.14,z:1.01,i:"b",e:416,s:356,o:"149"},{f:"q",y:2.14,z:1.01,i:"b",e:0,s:71,o:"162"},{y:2.14,i:"b",s:234,z:0,o:"152",f:"q"},{f:"q",p:2,y:3.15,z:0.2,i:"ActionHandler",e:{a:[{i:0,b:"kTimelineDefaultIdentifier",p:9,symbolOid:"2"}]},s:{a:[{p:7,b:"kTimelineDefaultIdentifier",symbolOid:"2"},{p:4,h:"137"}]},o:"kTimelineDefaultIdentifier"},{y:3.15,i:"b",s:416,z:0,o:"149",f:"q"},{y:3.15,i:"b",s:0,z:0,o:"162",f:"q"},{f:"q",y:3.18,z:0.17,i:"e",e:0,s:1,o:"139"},{y:4.05,i:"e",s:0,z:0,o:"139",f:"q"},{f:"q",p:2,y:4.05,z:0,i:"ActionHandler",s:{a:[{i:0,b:"kTimelineDefaultIdentifier",p:9,symbolOid:"2"},{p:4,h:"138"}]},o:"kTimelineDefaultIdentifier"}],f:30,b:[]}},bZ:180,O:["166","139","162","164","156","158","144","143","141","165","163","153","145","140","147","146","154","152","157","161","159","155","148","160","151","149","150","142"],n:"Untitled Layout","_":0,v:{"165":{c:856,d:72,I:"Solid",e:0.8,J:"Solid",K:"Solid",g:"#141414",L:"Solid",M:0,bF:"162",N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,O:0,C:"#D8DDE4",z:1,k:"div",D:"#D8DDE4",a:-6,b:164},"157":{c:785,d:189,I:"Solid",J:"Solid",K:"Solid",g:"#002649",L:"Solid",M:0,i:"Home-Color",bF:"156",N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,O:0,C:"#D8DDE4",z:1,k:"div",D:"#D8DDE4",a:0,b:171},"149":{x:"visible",dY:[["data-clip-path",".venueBlockMask"]],k:"div",c:1920,d:67,z:2,a:75,j:"absolute",bF:"139",b:356},"140":{x:"visible",a:75,b:234,j:"absolute",bF:"139",cP:"centerBlockMask",dC:{path:[[0,189,0,189,1920,189,1920,189],[1920,189,1920,189,1920,0,1920,0],[1920,0,1920,0,0,0,0,0],[0,0,0,0,0,189,0,189]],closed:true},z:6,d:189,k:"div",cQ:1,dD:0,c:1920,cR:1,dE:"#D8DDE4"},"161":{aU:8,G:"#FFF",aV:8,r:"inline",s:"Zuume",t:69,u:"normal",Z:"break-word",v:"normal",i:"Home-School-Name",w:"DREXEL<br>",bF:"159",j:"absolute",x:"visible",yy:"nowrap",k:"div",y:"preserve",z:2,aS:8,aT:8,a:0,F:"left",b:0},"153":{h:"135",p:"no-repeat",x:"visible",R:"#000",q:"100% 100%",a:56,j:"absolute",bF:"152",r:"none",T:4,b:-24,d:237,z:3,dB:"img",Q:0,S:0,k:"div",c:237,gg:"0"},"145":{c:785,d:189,I:"Solid",J:"Solid",K:"Solid",g:"#800000",L:"Solid",M:0,i:"Away-Color",bF:"143",N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,O:0,C:"#D8DDE4",z:1,k:"div",D:"#D8DDE4",a:75,b:157},"166":{c:1920,d:566,I:"Solid",J:"Solid",K:"Solid",g:"",L:"Solid",M:0,N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,k:"div",C:"#D8DDE4",z:1,O:0,D:"#D8DDE4",a:0,b:498},"158":{w:"",h:"97",p:"no-repeat",x:"visible",a:333,q:"100% 100%",b:87,j:"absolute",r:"inline",z:3,bF:"156",dB:"img",d:532,i:"Home-Logo",k:"div",c:532},"141":{x:"visible",a:588,b:124,j:"absolute",bF:"139",cP:"sponsorMask",k:"div",dC:{path:[[0,110,0,110,0,0,0,0],[0,0,0,0,896,0,896,0],[896,0,896,0,891,110,891,110],[891,110,891,110,0,110,0,110]],closed:true},d:110,z:9,c:896,dD:0,dE:"#D8DDE4"},"162":{x:"visible",dY:[["data-clip-path",".sponsorMask"]],k:"div",c:856,d:400,z:3,a:613,j:"absolute",bF:"139",b:71},"154":{c:350,d:189,I:"Solid",e:0.8,J:"Solid",K:"Solid",g:"#141414",L:"Solid",M:0,bF:"152",N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,O:0,C:"#D8DDE4",z:1,k:"div",D:"#D8DDE4",a:0,b:0},"146":{x:"visible",k:"div",c:263,d:174,z:3,a:581,j:"absolute",bF:"143",b:273},"159":{x:"visible",k:"div",c:263,d:174,z:2,a:25,j:"absolute",bF:"156",b:273},"150":{aU:8,G:"#000",aV:8,r:"inline",s:"'Zuume Medium'",t:46,u:"normal",Z:"break-word",v:"normal",i:"venueText",w:"DASKALAKIS ATHLETIC CENTER - PHILADELPHIA, PA",bF:"149",j:"absolute",x:"visible",yy:"nowrap",k:"div",y:"preserve",z:2,aS:8,aT:8,a:637,b:0},"142":{x:"visible",a:75,b:423,j:"absolute",r:"inline",cP:"venueBlockMask",dC:{path:[[0,0,0,0,1920,0,1920,0],[1920,0,1920,0,1920,87,1920,87],[1920,87,1920,87,0,87,0,87],[0,87,0,87,0,0,0,0]],closed:true},z:4,d:87,bF:"139",k:"div",dD:0,c:1920,dE:"#D8DDE4"},"163":{aU:8,G:"#FFF",aV:8,r:"inline",s:"Zuume",t:46,Z:"break-word",i:"sponsorText",w:"DREXEL BASKETBALL PRESENTED BY",bF:"162",j:"absolute",x:"visible",yy:"nowrap",k:"div",y:"preserve",z:2,aS:8,aT:8,a:6,b:166},"155":{h:"131",p:"no-repeat",x:"visible",a:25,dB:"img",q:"100% 100%",j:"absolute",r:"inline",z:2,bF:"152",b:47,d:96,k:"div",c:299},"147":{aU:8,G:"#FFF",c:395,aV:8,r:"inline",d:75,s:"Zuume",t:69,u:"normal",Z:"break-word",v:"normal",i:"Away-School-Name",w:"CHARLESTON<br>",bF:"146",j:"absolute",x:"visible",k:"div",y:"preserve",z:2,aS:8,aT:8,a:-149,F:"right",b:0},"139":{x:"visible",k:"div",c:2075,d:595,z:2,e:1,a:-75,j:"absolute",b:532},"151":{c:1920,d:61,I:"Solid",J:"Solid",K:"Solid",g:"#F0F0F0",L:"Solid",M:0,bF:"149",N:0,A:"#D8DDE4",x:"visible",j:"absolute",B:"#D8DDE4",P:0,O:0,C:"#D8DDE4",z:1,k:"div",D:"#D8DDE4",a:0,b:3},"143":{x:"visible",dY:[["data-clip-path",".centerBlockMask"]],k:"div",c:860,d:503,z:8,r:"inline",a:0,j:"absolute",bF:"139",b:267},"164":{h:"121",p:"no-repeat",x:"visible",a:456,dB:"img",q:"100% 100%",j:"absolute",r:"inline",z:3,bF:"162",b:0,d:400,k:"div",c:400},"156":{x:"visible",dY:[["data-clip-path",".centerBlockMask"]],k:"div",c:865,d:532,z:7,r:"inline",a:1210,j:"absolute",bF:"139",b:253},"148":{aU:8,G:"#FFF",c:360,aV:8,r:"inline",d:94,s:"Zuume",t:85,u:"normal",Z:"break-word",v:"bold",i:"Away-Team-Name",w:"COUGARS<br>",bF:"146",j:"absolute",x:"visible",k:"div",y:"preserve",z:1,aS:8,aT:8,a:-114,F:"right",b:64},"160":{aU:8,G:"#FFF",aV:8,r:"inline",s:"Zuume",t:85,u:"normal",Z:"break-word",v:"bold",i:"Home-Team-Name",w:"DRAGONS<br>",bF:"159",j:"absolute",x:"visible",yy:"nowrap",k:"div",y:"preserve",z:1,aS:8,aT:8,a:0,F:"left",b:64},"152":{x:"visible",dY:[["data-clip-path",".centerBlockMask"]],k:"div",c:350,d:189,z:5,a:860,j:"absolute",bF:"139",b:423},"144":{h:"91",p:"no-repeat",x:"visible",a:0,dB:"img",q:"100% 100%",j:"absolute",r:"inline",z:2,bF:"143",b:116,d:503,i:"Away-Logo",k:"div",c:503}}}],{},h,{q:{p:0,q:[[0,0,0.165,0.84,0.44,1,1,1]]},"113":{p:0,q:[[0,0,0.06008,0.9875,0.1007,0.9984,1,1]]}},null,false,false,-1,true,true,false,true,true);d[f]=c.API;document.getElementById(g).setAttribute("HYP_dn",f);c.z_o(this.body)})();})();
