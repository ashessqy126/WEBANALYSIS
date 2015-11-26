'use strict';
angular.module('webanalysisApp')
    .controller('LinkanaCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
    	var url = 'http://localhost:8000/get_analysis_link/';
        var circle = new circleDonutChart('linkana_progress');
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
                    $scope.msg = '工作中断或停止，请回主页重新开启分析';
                    circle.draw({
                        end: 1
                    });
                } else if (response.status === 1) {
                	$scope.msg = '恶意链接分析工作已完成，危险链接' + response.dangercount + '个';
                    circle.draw({
                        end: 100
                    });
                    $scope.results = response.results;
                    
                } else {
                	$scope.msg = '正在分析'+ response.link + "。。。，第" + response.count + '个/总共' +response.allcount+'，危险链接'+response.dangercount+'个';
                   	var percent = 100*response.count / response.allcount;
                   	circle.draw({
                        end: percent
                    });
                    $scope.results = response.results;
                    $timeout($scope.getstatus, 500);
                }
            }).error(function(e) {
                window.alert("网络错误");
            });
        };
        $timeout($scope.getstatus, 1500);
    }]);
