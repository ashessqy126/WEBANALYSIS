'use strict';

angular.module('webanalysisApp')
    .controller('BadcodeCtrl', ['$scope', '$http',function($scope, $http) {
    	var badcode = 'http://localhost:8000/badcode/?website=';
    	var circle = new circleDonutChart('badcode_progress');
        circle.draw({
            end: 0,
            start: 0,
            maxValue: 100,
            titlePosition: "outer-top",
            titleText: "进度",
            outerCircleColor: '#0085C8',
            innerCircleColor: '#004081'
        });
        $http.get(badcode + localStorage.website).success(function(response){
        	if(response.status == 0){
        		$scope.msg = '分析完成';
        		$scope.results = response.result;
        		circle.draw({
        			end:100
        		});
        	}
        	else{
        		circle.draw({
        			end:1
        		});
        		$scope.msg = '分析错误。。。';
        	}
        }).error(function(err){
        	window.alert('网络错误');
        });
  }]);