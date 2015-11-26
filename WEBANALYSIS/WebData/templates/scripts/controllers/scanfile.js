'use strict';

angular.module('webanalysisApp')
    .controller('ScanfileCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
        var url = 'http://localhost:8000/get_scansrc_status/'
        var circle = new circleDonutChart('scanfile_progress');
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
                    $scope.msg = '工作中断或停止，请回主页重新开启分析。';
                    circle.draw({
                        end: 1
                    });
                } else if (response.status === 1) {
                    $scope.msg = '文件扫描工作已完成，危险资源' + response.dangercount + '个';
                    circle.draw({
                        end: 100
                    });
                    $scope.results = response.result;

                } else {
                    $scope.msg = '正在扫描,第' + response.count + '个/总共' + response.allcount + '个，危险资源' + response.dangercount + '个';
                    var percent = 100 * response.count / response.allcount;
                    circle.draw({
                        end: percent
                    });
                    $scope.results = response.result;
                    $timeout($scope.getstatus, 500);
                }
            }).error(function(e) {
                window.alert("网络错误");
            });
        };
        $timeout($scope.getstatus, 1000);
    }]);
