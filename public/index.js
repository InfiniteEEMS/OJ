var app = angular.module("myApp", ['ngRoute']).controller("listCtrl", function($scope,$http,$route) {

        $scope.$route = $route;

        $http({
            method: 'GET',
            url: 'http://localhost:3000/api/v1/problems'
        }).then( (response) => {
            console.log("Get Problems suc ");
            $scope.problems = response.data;
        }, (response) => {
            console.log("Get Problems fail ");
        });

}).controller("codeCtrl", function($scope, $route) {

    $scope.$route = $route;
    
    $scope.message = "Type your message here..";

}).config( ($routeProvider) =>{

    $routeProvide.when('/problemlist', {
        templateUrl: 'problemlist.html',
        controller: 'listCtrl'
    })
    .when('/editsolution', {
        templateUrl: 'editsolution.html',
        controller: 'codeCtrl'
    })
    .otherwise({
         redirectTo: '/problemlist'
    })

})
