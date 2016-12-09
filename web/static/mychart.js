Highcharts.setOptions({
	global: {useUTC: false}
});
var chart1;
var count = 0;
var time = [];
var weekName = ["Mon","Tue","Wed","Thr","Fri","Sat","Sun"];


function getOnlineInfo(userID,userName,date){
	time = [];
	var isOnline = new Array(1440);
	isOnline.fill(0);
	$.getJSON( "http://localhost:5000/api/v1.0/getOnlineInfo/"+date+"/"+userID, function(data) {
		$.each( data.online_data, function( i, item ) {
		  		isOnline[item] = 1;
		    });
		})
		.always(function(data) {
			for (var i=0; i<1440; i++){
	        	var d = new Date(2016,11,7);
	            time.push([d.getTime()+i*60*1000,isOnline[i]]);
	        }
	        addSeries(userName);
		});
}

function getOnlineCount(week){
	if(week >6)
		return;
	time = [];
	$.getJSON( "http://localhost:5000/api/v1.0/getCount/"+week)
		.always(function(data) {
			for (var i=0; i<1440; i++){
	        	var d = new Date(2016,11,7);
	            time.push([d.getTime()+i*60*1000, (data[i]=="")?0:parseInt(data[i])]);
	        }
	        addSeriesWeek(parseInt(week));
	        getOnlineCount(week+1);
		});
}

function ChartInit(){
	chart1 = Highcharts.stockChart('container', {
		chart: {
	        zoomType: 'x' ,
	        panning: 'x',
	        panKey: 'shift'
	    },
	    title: {
            text: '<b>Facebook好友上線資訊</b>'
        },
	    xAxis: {
			type: 'datetime'
		},
		credits: {
	        enabled: false
	    },
		rangeSelector: {
			allButtonsEnabled:true,
			inputEnabled:false,
			buttonTheme: { // styles for the buttons
	            fill: 'none',
	            stroke: 'none',
	            'stroke-width': 0,
	            r: 10,
	            style: {
	                color: '#039',
	                fontWeight: 'bold'
	            },
	            states: {
	                hover: {
	                },
	                select: {
	                    fill: '#039',
	                    style: {
	                        color: 'white'
	                    }
	                }
	            }
	        },
			buttons: [{
				type: 'minute',
				count: 60,
				text: 'min'
			}, {
				type: 'hour',
				count: 6,
				text: 'hour'
			}, {
				type: 'minute',
				count: 1439,
				text: 'day'
			}],
			selected: 2
	    },
	    tooltip: {
	        valueDecimals: 2,
	        xDateFormat: '%A, %b %e , %H:%M',
	        shared: true
	    }
	});
}

function ChartInitWeek(){
	chart1 = Highcharts.stockChart('container', {
		chart: {
	        zoomType: 'x' ,
	        panning: 'x',
	        panKey: 'shift'
	    },
	    title: {
            text: '<b>上線人數統計圖</b>'
        },
	    xAxis: {
			type: 'datetime',
			dateTimeLabelFormats: {
				millisecond: '%H:%M',
				second: '%H:%M',
				minute: '%H:%M',
				hour: '%H:%M',
				day: '%H:%M',
				week: '%H:%M',
				month: '%H:%M',
				year: '%H:%M'
			}
		},
		credits: {
	        enabled: false
	    },
		rangeSelector: {
			allButtonsEnabled:true,
			inputEnabled:false,
			buttonTheme: { // styles for the buttons
	            fill: 'none',
	            stroke: 'none',
	            'stroke-width': 0,
	            r: 10,
	            style: {
	                color: '#039',
	                fontWeight: 'bold'
	            },
	            states: {
	                hover: {
	                },
	                select: {
	                    fill: '#039',
	                    style: {
	                        color: 'white'
	                    }
	                }
	            }
	        },
			buttons: [{
				type: 'minute',
				count: 60,
				text: 'min'
			}, {
				type: 'hour',
				count: 6,
				text: 'hour'
			}, {
				type: 'minute',
				count: 1439,
				text: 'day'
			}],
			selected: 2
	    },
	    tooltip: {
	        valueDecimals: 2,
	        xDateFormat: '%H:%M',
	        shared: true
	    }
	});
}

function addSeries(userName) {
	chart1.addSeries({
     	tooltip: {
         	pointFormatter:function(){
         		if(this.y==1)
         			return '<span style="color:#003C9D">'+userName+'</span>: <span style="color:red;font-weight: bold">online</b><br/>';
         		else
         			return '<span style="color:#003C9D"">'+userName+'</span>: <b>offline</b><br/>';
         	}
        },
        name: userName,
        data: time,
        animation: {
            duration: 1100+count
        }
    }, true, {
        duration: 2000+count,
        easing: 'easeOutBounce'
    });
    count++;
};

function addSeriesWeek(week) {
	chart1.addSeries({
     	tooltip: {
         	pointFormat:'<span style="color:#003C9D">'+weekName[week]+'</span>: <span style="color:red;font-weight: bold">{point.y}人</b><br/>'
        },
        name: week,
        data: time,
        animation: {
            duration: 1100+count
        }
    }, true, {
        duration: 2000+count,
        easing: 'easeOutBounce'
    });
    count++;
};

function removeSeries(userName){
	for(var i=0 ; i<chart1.series.length; i++){
		if(userName == chart1.series[i].name){
			chart1.series[i].remove();
			break;
		}
	}
}

function removeAllSeries(){
	var temp = chart1.series.length;
	for(var i=0 ; i<temp-1; i++){
		chart1.series[0].remove();
	}
}
