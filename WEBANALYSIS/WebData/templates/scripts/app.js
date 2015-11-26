'use strict';

/**
 * @ngdoc overview
 * @name webanalysisApp
 * @description
 * # webanalysisApp
 *
 * Main module of the application.
 */
angular
  .module('webanalysisApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        controllerAs: 'home'
      })
      .when('/start',{
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .when('/start/linkana', {
        templateUrl: 'views/linkana.html',
        controller: 'LinkanaCtrl',
        controllerAs: 'linkana'
      })
      .when('/start/scanfile', {
        templateUrl: 'views/scanfile.html',
        controller: 'ScanfileCtrl',
        controllerAs: 'scanfile'
      })
      .when('/start/badcode', {
        templateUrl: 'views/badcode.html',
        controller: 'BadcodeCtrl',
        controllerAs: 'badcode'
      })
      .when('/start/watchsys',{
        templateUrl: 'views/watchsys.html',
        controller: 'WatchsysCtrl',
        controllerAs: 'watchsys'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
