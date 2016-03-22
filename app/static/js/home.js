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
            })
            .state('moudle_create', {
                url: '/moudle_create/:appId',
                templateUrl: 'static/temp/moudle_create.html',
                controller: 'moudle_createCtl'
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
    .controller('app_detailCtl', function ($scope, $http,$stateParams,$state) {
        $scope.appId = $stateParams.app_id;
        $http.get("/apps/select",{params: {appId:$scope.appId}
            })
            .success(function (response) {
                $scope.app = response.app;
            });
        $http.get("/moudles/list",{params: {appId:$scope.appId}
            })
            .success(function (response) {
                $scope.moudles = response.moudles;
            });
        $scope.create_moudle = function () {
            $state.go('moudle_create',{appId:$scope.appId });
        };
    })
    .controller('moudle_createCtl', function ($scope, $http, $stateParams,$state) {
        $scope.moudle={};
        $scope.moudle.appId = $stateParams.appId;
        $scope.create = function () {
            
            $http.post("/moudles/new", $scope.moudle)
                .success(function (response) {
                    $state.go('app_detail',{app_id:'1'});
                });
        };
    });