var map;
var places=[];

//初始化地图
function init(){
    map=new BMap.Map("container");
//    map.centerAndZoom(new BMap.Point(116.404, 39.915), 14);
    // map.setCurrentCity("武汉");
    map.addControl(new BMap.MapTypeControl());   //添加地图类型控件
    map.enableScrollWheelZoom(true);             //开启鼠标滚轮缩放
    var lng , lat ;
    var geolocation = new BMap.Geolocation();
    geolocation.getCurrentPosition(function(r){
        if(this.getStatus() == BMAP_STATUS_SUCCESS){
            lng = r.point.lng;
            lat = r.point.lat;
            map.centerAndZoom(new BMap.Point(lng, lat), 11);
            var mk = new BMap.Marker(r.point);
            map.addOverlay(mk);
          }
          else {
            alert('failed'+this.getStatus());
          }        
       });
    //输入提示
	Add("start");
    Add("end");
    Add("place");

}
function DrivingQuery(){
    map.clearOverlays();
    var start1=document.getElementById("start").value;
    var end1=document.getElementById("end").value;
    //创建地址解析器实例
    var myGeo = new BMap.Geocoder();
    // 将地址解析结果显示在地图上，并调整地图视野
    myGeo.getPoint(start1, function(point1){
        if(point1){
            var myGeo1 = new BMap.Geocoder();
    // 将地址解析结果显示在地图上，并调整地图视野
    myGeo1.getPoint(end1, function(point2){
        if(point2){
            var dr=new BMap.DrivingRoute(map);
    var tk=0;
    dr.search(point1,places[0]);
    for(var k=0;k<places.length-1;k++){
        dr.search(places[k],places[k+1]);
    }
    dr.search(places[places.length-1],point2);
    dr.setSearchCompleteCallback(function(){
        var pts = dr.getResults().getPlan(0).getRoute(0).getPath();    //通过驾车实例，获得一系列点的数组
        tk+=dr.getResults().getPlan(0).getDistance(false);
        // alert(tk);
        var polyline = new BMap.Polyline(pts);     
        map.addOverlay(polyline);
        var m=[];
        map.addOverlay(new BMap.Marker(point1));
        for(var k=0;k<places.length;k++){
            map.addOverlay(new BMap.Marker(places[k]));
        }
        map.addOverlay(new BMap.Marker(point2));
        map.addOverlay(new BMap.Label("起点",{position:point1}));
        for(var k=0;k<places.length;k++){
            map.addOverlay(new BMap.Label("途径点"+k,{position:places[k]}));
        }
        map.addOverlay(new BMap.Label("终点",{position:point2}));
        m.push(point1);
        for(var k=0;k<places.length;k++){
           m.push(places[k]);
        }
        m.push(point2);
        setTimeout(function(){
            map.setViewport(m);          //调整到最佳视野
        },1000);
        
    });
        }else{
            alert('您选择的地址没有解析到结果！');
        }
    }, '武汉市')
        }else{
            alert('您选择的地址没有解析到结果！');
        }
    }, '武汉市')
    
    // var pt1=new BMap.Point(116.433,40,0);
    // var pt2=new BMap.Point(116.413,40,02);
    // var waypoints="";
    // waypoints+=places[0];
    // waypoints.push(places[1]);
    // var output = "从西单到上地驾车需要";
    //     var searchComplete = function (results){
    //         if (driving.getStatus() != BMAP_STATUS_SUCCESS){
    //             return ;
    //         }
    //         var plan = results.getPlan(0);
    //         output += plan.getDuration(true) + "\n";                //获取时间
    //         output += "总路程为：" ;
    //         output += plan.getDistance(true) + "\n";             //获取距离
    //         alert(output);
    //     }
    // var driving = new BMap.DrivingRoute(map, {renderOptions:{map: map,panel:"r-result", autoViewport: true},onSearchComplete: searchComplete});
    // driving.search(start,end,{waypoints:waypoints});
    // driving.search(start,end);
    

}
function WalkingQuery(){
    map.clearOverlays();
    var start=document.getElementById("start").value;
    var end=document.getElementById("end").value;
    // var output = "需要";
    //     var searchComplete = function (results){
    //         if (walking.getStatus() != BMAP_STATUS_SUCCESS){
    //             return ;
    //         }
    //         var plan = results.getPlan(0);
    //         output += plan.getDuration(true) + "\n";                //获取时间
    //         output += "总路程为：" ;
    //         output += plan.getDistance(true) + "\n";             //获取距离
    //         alert(output);
    //     }
    var walking = new BMap.WalkingRoute(map, {renderOptions:{map: map,panel:"r-result", autoViewport: true}});
    walking.search(start,end);
    
}
function BusQuery(){
    map.clearOverlays();
    var start1=document.getElementById("start").value;
    var end1=document.getElementById("end").value;
    //创建地址解析器实例
    var myGeo = new BMap.Geocoder();
     // 将地址解析结果显示在地图上，并调整地图视野
     myGeo.getPoint(start1, function(point1){
        if(point1){
            var myGeo1 = new BMap.Geocoder();
        myGeo1.getPoint(end1, function(point2){
        if(point2){
            var transit = new BMap.TransitRoute(map, {renderOptions:{map: map,panel:"r-result", autoViewport: true}});
            transit.search(point1,point2);
        }else{
            alert('您选择的地址没有解析到结果！');
        }
    }, '武汉市')
        }else{
            alert('您选择的地址没有解析到结果！');
        }
    }, '武汉市')
    
    // var transit = new BMap.TransitRoute(map, {renderOptions:{map: map,panel:"r-result", autoViewport: true}});
    // transit.search(start,end);
}
function G(id) {
    return document.getElementById(id);
}

function setPlace(){
    map.clearOverlays();    //清除地图上所有覆盖物
    function myFun(){
        var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
        map.centerAndZoom(pp, 18);
        map.addOverlay(new BMap.Marker(pp));    //添加标注
    }
    var local = new BMap.LocalSearch(map, { //智能搜索
      onSearchComplete: myFun
    });
    local.search(myValue);
}
function Add(x){
    var ac = new BMap.Autocomplete(    //建立一个自动完成的对象
		{"input" : x
		,"location" : map
	});

	ac.addEventListener("onhighlight", function(e) {  //鼠标放在下拉列表上的事件
	var str = "";
		var _value = e.fromitem.value;
		var value = "";
		if (e.fromitem.index > -1) {
			value = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
		}    
		str = "FromItem<br />index = " + e.fromitem.index + "<br />value = " + value;
		
		value = "";
		if (e.toitem.index > -1) {
			_value = e.toitem.value;
			value = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
		}    
		str += "<br />ToItem<br />index = " + e.toitem.index + "<br />value = " + value;
		G("searchResultPanel").innerHTML = str;
	});

	var myValue;
	ac.addEventListener("onconfirm", function(e) {    //鼠标点击下拉列表后的事件
	var _value = e.item.value;
		myValue = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
		G("searchResultPanel").innerHTML ="onconfirm<br />index = " + e.item.index + "<br />myValue = " + myValue;
		
		setPlace();
	});
}
function mine(){
    //投影实例
        var projection = map.getMapType().getProjection();

        // 地图div宽高
        var box = map.getSize()
        var zoom = window.Math.pow(2, 18 - map.getZoom());

        // 中心坐标 转 平面坐标
        var center = projection.lngLatToPoint(map.getCenter());

        //元素左上角位置
        var left = 100;
        var top = 100;
        var x = (left - box.width / 2) * zoom + center.x;
        var y = center.y - (top - box.height / 2) * zoom;
        var NW = map.getMapType().getProjection().pointToLngLat({
            x: x,
            y: y
        });
        //坐标点
        var point = new BMap.Point(NW.lng, NW.lat);
        //创建图像标注
        map.addOverlay(new BMap.Marker(point));
        alert('lng:'+NW.lng+',lat:'+NW.lat);

}
//地图上添加途径点
function Add_place(){
    //map.clearOverlays();
    var place=document.getElementById("place").value;
    //创建地址解析器实例
    var myGeo = new BMap.Geocoder();
    // 将地址解析结果显示在地图上，并调整地图视野
    myGeo.getPoint(place, function(point){
        if(point){
            map.centerAndZoom(point, 16);
            map.addOverlay(new BMap.Marker(point));
            places.push(point);
            //alert(places.length);
        }else{
            alert('您选择的地址没有解析到结果！');
        }
    }, '武汉市')
}
//路径优化-未实现
function Route_optimize(){
    //alert(places.length);
    var Route=new Array();
    var Routes=new Array();
    var num=places.length;
    alert("num="+num);
    
    
    var dr=new BMap.DrivingRoute(map);
    //test
    
    var disresult = new Array(24).fill(0);
    //test
    var min=Number.MAX_VALUE;
    var min_route=new Array();
    var i=0;
    while(i<24){
        var places2=new Array();
        for(var n=0;n<num;n++){
            places2[n]=n;
        }

        // alert("第一个点"+Math.floor(i/6)+"第二个点"+Math.floor((i%6)/2)+"第三个点"+Math.floor((i%6)%2)+"第四个点"+0);
        Route[0]=places2[Math.floor(i/6)];
        // alert(places2[Math.floor(i/6)]);
        // alert(Route[0])
        places2.splice(Math.floor(i/6),1);

        Route[1]=places2[Math.floor((i%6)/2)];
        // alert(places2[Math.floor((i%6)/2)]);
        // alert(Route[1]);
        places2.splice(Math.floor((i%6)/2),1);

        Route[2]=places2[Math.floor((i%6)%2)];
        places2.splice(Math.floor((i%6)%2),1);

        Route[3]=places2[0];
        places2.splice(0,1);
        // Routes.push(Route);
        // alert("i= "+i+" "+Route);

        tk=0;
        Routes[i]=Route;
        // alert(" 顺序为"+Route[0]+Route[1]+Route[2]+Route[3]);
        cs=0;
        // for(var m=0;m<3;m++){
        //     dr.search(places[Route[m]],places[Route[m+1]]);
        //     // alert("Route[m]="+Route[m]);
        //     // alert("Route[m+1]="+Route[m+1]);

        // }
        //*********************************************************************************************** */
        dr.setSearchCompleteCallback(function(){
            cs++;
            tk+=dr.getResults().getPlan(0).getDistance(false);
            //  alert(dr.getResults().getPlan(0).getDistance(false));
            // alert(tk);
            if(cs%3==0){
                if(tk<min){
                    min=tk;
                    alert("这条路更短距离为："+tk+" 顺序为"+Route[0]+Route[1]+Route[2]+Route[3]);
                    
                }
                tk=0;
            }
            
        });
         //************************************************************************************************/
         let promise = new Promise(function(resolve, reject){
            dr.search(places[Route[0]],places[Route[1]]);
            dr.search(places[Route[1]],places[Route[2]]);
            dr.search(places[Route[2]],places[Route[3]]);
            if(dr.getStatus()==0){
                resolve()
            }
            else{
                reject(console.error());
            }
            
        });
        promise.then(() => i++);
        

        // if(tk[i]<min){
        //     min=tk[i];
        //     alert("这条路更短距离为："+tk[i]);
        //     map.clearOverlays();
    
        //     var m2 = new BMap.Marker(places[Route[0]]);
        //     var m3 = new BMap.Marker(places[Route[1]]);
        //     var m4 = new BMap.Marker(places[Route[2]]);
        //     var m5 = new BMap.Marker(places[Route[3]]);
        //     map.addOverlay(m2);
        //     map.addOverlay(m3);
        //     map.addOverlay(m4);
        //     map.addOverlay(m5);
            
        //     var lab2 = new BMap.Label("起点",{position:places[Route[0]]});
        //     var lab3 = new BMap.Label("途径点1",{position:places[Route[1]]});
        //     var lab4 = new BMap.Label("途径点2",{position:places[Route[2]]});
        //     var lab5 = new BMap.Label("终点",{position:places[Route[3]]})
        //     map.addOverlay(lab2);
        //     map.addOverlay(lab3);
        //     map.addOverlay(lab4);
        //     map.addOverlay(lab5);
        //     }
    }
    // var dr=new BMap.DrivingRoute(map);
    // var takes=0;
    // dr.search(places[0],places[1]);
    // dr.search(places[1],places[2]);
    // dr.search(places[2],places[3]);
    // dr.setSearchCompleteCallback(function(){
    //     var pts = dr.getResults().getPlan(0).getRoute(0).getPath();    //通过驾车实例，获得一系列点的数组
    //     alert(dr.getResults().getPlan(0).getDistance(false));
    //     takes+=dr.getResults().getPlan(0).getDistance(false);
    //     alert(takes);
    //     var polyline = new BMap.Polyline(pts);     
    //     map.addOverlay(polyline);         //创建3个marker
    //     var m2 = new BMap.Marker(places[0]);
    //     var m3 = new BMap.Marker(places[1]);
    //     var m4 = new BMap.Marker(places[2]);
    //     var m5 = new BMap.Marker(places[3]);
    //     // map.addOverlay(m1);
    //     map.addOverlay(m2);
    //     map.addOverlay(m3);
    //     map.addOverlay(m4);
    //     map.addOverlay(m5);
    //     // map.addOverlay(m6);
        
    //     // var lab1 = new BMap.Label("起点",{position:start});        //创建3个label
    //     var lab2 = new BMap.Label("起点",{position:places[0]});
    //     var lab3 = new BMap.Label("途径点",{position:places[1]});
    //     var lab4 = new BMap.Label("途径点",{position:places[2]});
    //     var lab5 = new BMap.Label("终点",{position:places[3]});
    //     // var lab6 = new BMap.Label("终点",{position:end});
    //     // map.addOverlay(lab1);
    //     map.addOverlay(lab2);
    //     map.addOverlay(lab3);
    //     map.addOverlay(lab4);
    //     map.addOverlay(lab5);
    //     // map.addOverlay(lab6);
        
    //     setTimeout(function(){
    //         map.setViewport([places[0],,places[1],places[2],places[3]]);          //调整到最佳视野
    //     },1000);
        
    // });
  
}
