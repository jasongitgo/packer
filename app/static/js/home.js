var routeApp = angular.module('routeApp', ['ui.router'])
    .config(function ($stateProvider, $urlRouterProvider) {

        $stateProvider


            .state('index', {
                url: '/index',
                views: {
                    'main': {
                        templateUrl: 'static/temp/home.html',
                        controller: 'indexCtl'
                    },
                    'apps_list': {
                        templateUrl: 'static/temp/app_list.html',
                        controller: 'apps_list'
                    }
                }
            })

            .state('create_app', {
                url: '/create_app',
                templateUrl: 'static/temp/app_create.html',
                controller: 'app_createCtl'
            })
            .state('app_detail', {
                url: '/app_detail/:app_id',
                templateUrl: 'static/temp/app_detail.html',
                controller: 'app_detailCtl'
            });

        // catch all route
        // send users to the form page
        $urlRouterProvider.otherwise('/index');
    })

    // our controller for the form
    // =============================================================================
    .controller('indexCtl', ['$scope', '$state', function ($scope, $state) {
        $scope.show_app_create = function () {
            $state.go('create_app');
        };
    }])
    .controller('app_createCtl', function ($scope, $http, $state) {
        $scope.create = function () {
            $http.post("/apps/new", $scope.app)
                .success(function (response) {
                    $state.go('index');
                });
        };
    })
    .controller('apps_list', function ($scope, $http) {
        $http.get("/apps/list")
            .success(function (response) {
                $scope.apps = response.apps;
            });
    })
    .controller('app_detailCtl', function ($scope, $http) {
        $http.get("/apps/list")
            .success(function (response) {
                $scope.apps = response.apps;
            });
    });