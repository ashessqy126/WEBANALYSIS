'use strict';

/**
 * @ngdoc function
 * @name webanalysisApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the webanalysisApp
 */
angular.module('webanalysisApp')
    .controller('MainCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
        $scope.website = localStorage.website
        $scope.completed = false;
        var url = 'http://localhost:8000/checkflag/';
        var startscanfile = "http://localhost:8000/start_scansrc/?website="
        var timer = null;
        var startlinkana = 'http://localhost:8000/start_analysis_link/?website=';
        var circle = new circleDonutChart('progress');
        circle.draw({
            end: 0,
            start: 0,
            maxValue: 100,
            titlePosition: "outer-top",
            titleText: "进度",
            outerCircleColor: '#0085C8',
            innerCircleColor: '#004081'
        });
        $scope.getstatus = function() {
            $http.get(url).success(function(response) {
                if (response.status === -2) {
                	$scope.webstatus = '工作中断或停止，请回主页重新爬取。';
                	circle.draw({end:1});
                } else if (response.status === 4) {
                	circle.draw({end:100});
                    $scope.completed = true;
                } else {
        			if (response.status === 0){
        				$scope.webstatus = '正在初始化...';
        			}
                	else if(response.status === 1){
                		$scope.webstatus = '正在爬取网站中的链接，请稍后...';
                		circle.draw({end:10});
                	}
                	else if(response.status === 2){
                		$scope.webstatus = '正在爬取网站中的资源，请稍后...';
                		circle.draw({end:40});
                	}
                	else if(response.status ===3){
                		$scope.webstatus = '正在匹配网站中的代码，请稍后...';
                		circle.draw({end:70});
                	}
                    $timeout($scope.getstatus, 1000);
                }
            }).error(function(e) {
                window.alert("网络错误");
            });
        };
        $timeout($scope.getstatus, 1000);
        $scope.startlinkana = function(){
            $http.get(startlinkana + localStorage.website).success(function(response){
                
            });
        };
        $scope.startscanfile = function(){
            $http.get(startscanfile + localStorage.website).success(function(response){
                
            });
        };
    }]);
