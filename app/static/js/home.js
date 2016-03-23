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
                        templateUrl: 'static/temp/app/list.html',
                        controller: 'apps_list'
                    }
                }
            })

            .state('create_app', {
                url: '/create_app/:appId',
                templateUrl: 'static/temp/app/create.html',
                controller: 'app_createCtl'
            })
            .state('app_detail', {
                url: '/app_detail/:appId',
                templateUrl: 'static/temp/app/detail.html',
                controller: 'app_detailCtl'
            })
            .state('moudle_create', {
                url: '/moudle_create/:appId',
                templateUrl: 'static/temp/moudle/create.html',
                controller: 'moudle_createCtl'
            })
            .state('config_create', {
                url: '/config_create/?relateId&type',
                templateUrl: 'static/temp/config/create.html',
                controller: 'config_createCtl'
            })
            .state('cmd_template_create', {
                url: '/cmd_template_create/?relateId&type',
                templateUrl: 'static/temp/cmdTemplate/create.html',
                controller: 'cmd_template_createCtl'
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
    .controller('app_createCtl', function ($scope, $http, $state, $stateParams) {
        var id = $stateParams.appId;
        if (id) {
            $http.get("/common/select", {
                    params: {id: id, type: 'app'}
                })
                .success(function (response) {
                    $scope.app = response.entity;
                });
        }
        $scope.create = function () {
            $http.post("/common/new", {'type': 'app', 'entity': $scope.app})
                .success(function (response) {
                    if (id)
                        $state.go('app_detail', {appId: id});
                    else
                        $state.go('index');
                });
        };
    })
    .controller('apps_list', function ($scope, $http) {
        $http.get("/common/list", {
                params: {type: 'app'}
            })
            .success(function (response) {
                $scope.apps = response.entities;
            });
    })
    .controller('app_detailCtl', function ($scope, $http, $stateParams, $state) {
        $scope.appId = $stateParams.appId;
        $http.get("/common/select", {
                params: {id: $scope.appId, type: 'app'}
            })
            .success(function (response) {
                $scope.app = response.entity;
            });
        $http.get("/common/list", {
                params: {type: 'moudle', appId: $scope.appId}
            })
            .success(function (response) {
                $scope.moudles = response.entities;
            });
        $http.get("/common/list", {
                params: {type: 'config', relateId: $scope.appId}
            })
            .success(function (response) {
                $scope.configs = response.entities;
            });
        $http.get("/common/list", {
                params: {type: 'cmdtemplate', relateId: $scope.appId}
            })
            .success(function (response) {
                $scope.cmdTemplates = response.entities;
            });
        $scope.create_moudle = function () {
            $state.go('moudle_create', {appId: $scope.appId});
        };
        $scope.create_moudle = function () {
            $state.go('moudle_create', {appId: $scope.appId});
        };
        $scope.create_config = function () {
            $state.go('config_create', {relateId: $scope.appId,type:'app'});
        };
        $scope.create_cmd_template = function () {
            $state.go('cmd_template_create', {relateId: $scope.appId,type:'app'});
        };
    })
    .controller('moudle_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.moudle = {};
        $scope.moudle.appId = $stateParams.appId;
        $scope.create = function () {

            $http.post("/common/new", {type: 'moudle', entity: $scope.moudle})
                .success(function (response) {
                    $state.go('app_detail', {appId: $stateParams.relateId});
                });
        };
    })
    .controller('config_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.config = {};
        $scope.config.relateId = $stateParams.relateId;
        $scope.config.type = $stateParams.type;
        $scope.create = function () {

            $http.post("/common/new", {type: 'config', entity: $scope.config})
                .success(function (response) {
                    $state.go('app_detail', {appId: $stateParams.relateId});
                });
        };
    })
    .controller('cmd_template_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.template = {};
        $scope.template.relateId = $stateParams.relateId;
        $scope.template.type = $stateParams.type;
        $scope.template.isDefault = false;
        $scope.create = function () {

            $http.post("/common/new", {type: 'cmdtemplate', entity: $scope.template})
                .success(function (response) {
                    $state.go('app_detail', {appId: $stateParams.relateId});
                });
        };
    });