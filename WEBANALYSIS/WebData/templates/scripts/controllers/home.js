'use strict';

angular.module('webanalysisApp')
    .controller('HomeCtrl', ['$scope', '$http',function($scope, $http) {
    	var url = 'http://localhost:8000/startscan/?';
        var deleteCachesUrl = "http://localhost:8000/removeCaches/?";
        $scope.inputshow = true;
        $scope.hashis = false;
        $scope.progressshow = false;
        $scope.confirm = function() {
            if ($scope.website != null && $scope.domain != null) {
            	var re = new RegExp(/^((https?|ftp|news):\/\/)?([a-z]([a-z0-9\-]*[\.。])+([a-z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&]*)?)?(#[a-z][a-z0-9_]*)?$/);
            	var result = re.test($scope.website);
            	if (result){
                	$scope.inputshow = false;  
            	}
            	else{
            		window.alert('请输入以http://或者https://开头的正确网址');
            	}
            }
            else{
            	window.alert('请输入所有参数');
            }
        };
        $scope.deleteCaches = function(){
            $scope.progressshow = true;
            $http.get(deleteCachesUrl + 'website=' + $scope.website).success(function(response){
                $scope.progressshow = false;
                if(response.status = 0){
                    window.alert("清除成功！");
                }
                else{
                    window.alert("没有该缓存");
                }
                
            }).error(function(err){
                window.alert('网络错误');
            });
        };
        $scope.start=function(){
        	$http.get(url+'website=' + $scope.website + '&domain=' +$scope.domain).success(function(response){
        			if(response.status == 0){
                        window.location.href = '#/start';
                        localStorage.website = $scope.website;
                    }
                    else if(response.status == -2 ){
                        window.alert("正在进行中");
                        window.location.href = '#/start';
                    }
                    else{
                        window.alert("you must should input the website and domain");
                    }
        		}).error(function(err){
        			window.alert('网络错误');
        		});
        };
        if(localStorage.getItem('website')!=null){
            $scope.hashis = true;
        }
    }]);
