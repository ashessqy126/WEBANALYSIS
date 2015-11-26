'use strict';

angular.module('webanalysisApp')
    .controller('WatchsysCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout){
    	$scope.sys = {}
    	//$scope.status = 0 ;
    	var url = "http://localhost:8000/watchsys/"
    	$http.get(url).success(function(response){
    		$scope.sys = response;
    		//$scope.status = response.status;
    		if(response.status == 0){
    			$scope.info = '系统正常';
    		}
    		else if(response.status == 1){
    			$scope.info = '可能存在威胁'
    		}
    		else if(response.status == 2){
    			$scope.info = 'warning：可能存在比较大的威胁'
    		}
    		else if(response.status == 3){
    			$scope.info = 'danger:系统异常，可能存在大的危险！！'
    		}
    		else if(response.status == 4){
    			$scope.info = 'danger:系统异常，存在危险！！'
    		}
            $timeout(function(){
                $(".cpu").fadeIn("slow");
            },200);
            $timeout(function(){
                $(".mem").fadeIn("slow");
            },400);
            $timeout(function(){
                $(".swap").fadeIn("slow");
            },600);
            $timeout(function(){
                $(".disk").fadeIn("slow");
            },800);
            $timeout(function(){
                $(".sys_status").fadeIn("slow");
            },1000);
    	}).error(function(error){
    		window.alert('网络错误');
    	});
    }]);