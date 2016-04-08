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
            .state('moudle_detail', {
                url: '/moudle_detail/:id',
                templateUrl: 'static/temp/moudle/detail.html',
                controller: 'moudle_detailCtl'
            })
            .state('config_create', {
                url: '/config_create/?relateId&type',
                templateUrl: 'static/temp/config/create.html',
                controller: 'config_createCtl'
            })
            .state('config_detail', {
                url: '/config_detail/?id&relateId&type',
                templateUrl: 'static/temp/config/detail.html',
                controller: 'config_detailCtl'
            })
            .state('cmd_template_create', {
                url: '/cmd_template_create/?relateId&type&id',
                templateUrl: 'static/temp/cmdTemplate/create.html',
                controller: 'cmd_template_createCtl'
            })
            .state('cmd_template_detail', {
                url: '/cmd_template_detail/:id',
                templateUrl: 'static/temp/cmdTemplate/detail.html',
                controller: 'cmd_template_detailCtl'
            })
            .state('cmd_create', {
                url: '/cmd_create/?id&templateId',
                templateUrl: 'static/temp/cmd/create.html',
                controller: 'cmd_createCtl'
            })
            .state('pack_create', {
                url: '/pack_create/:appId',
                templateUrl: 'static/temp/pack/create.html',
                controller: 'pack_createCtl'
            })
            .state('task_list', {
                url: '/task_list',
                templateUrl: 'static/temp/pack/list.html',
                controller: 'task_listCtl'
            })
            .state('step_list', {
                url: '/step_list/:taskId',
                templateUrl: 'static/temp/pack/detail.html',
                controller: 'step_listCtl'
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
                    params: {id: id, _type: 'app'}
                })
                .success(function (response) {
                    $scope.app = response.entity;
                });
        }
        $scope.create = function () {
            $http.post("/common/new", {'_type': 'app', 'entity': $scope.app})
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
                params: {_type: 'app'}
            })
            .success(function (response) {
                $scope.apps = response.entities;
            });
    })
    .controller('app_detailCtl', function ($scope, $http, $stateParams, $state) {
        $scope.appId = $stateParams.appId;
        $http.get("/common/select", {
                params: {id: $scope.appId, _type: 'app'}
            })
            .success(function (response) {
                $scope.app = response.entity;
            });
        $http.get("/common/list", {
                params: {_type: 'moudle', appId: $scope.appId}
            })
            .success(function (response) {
                $scope.moudles = response.entities;
            });
        $http.get("/common/list", {
                params: {_type: 'config', relateId: $scope.appId, type: 'app'}
            })
            .success(function (response) {
                $scope.configs = response.entities;
            });
        $http.get("/common/list", {
                params: {_type: 'cmdtemplate', relateId: $scope.appId, type: 'app'}
            })
            .success(function (response) {
                $scope.cmdTemplates = response.entities;
            });
        $scope.change_app = function () {
            $state.go('create_app', {appId: $scope.appId});
        };
        $scope.create_moudle = function () {
            $state.go('moudle_create', {appId: $scope.appId});
        };
        $scope.create_config = function () {
            $state.go('config_create', {relateId: $scope.appId, type: 'app'});
        };
        $scope.create_cmd_template = function () {
            $state.go('cmd_template_create', {relateId: $scope.appId, type: 'app'});
        };
        $scope.pack = function () {
            $state.go('pack_create', {appId: $scope.appId});
        };
    })
    .controller('moudle_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.moudle = {};
        $scope.moudle.appId = $stateParams.appId;
        $scope.create = function () {

            $http.post("/common/new", {_type: 'moudle', entity: $scope.moudle})
                .success(function (response) {
                    $state.go('app_detail', {appId: $stateParams.appId});
                });
        };
    })
    .controller('moudle_detailCtl', function ($scope, $http, $stateParams, $state) {
        $scope.moudleId = $stateParams.id;
        $http.get("/common/select", {
                params: {id: $scope.moudleId, _type: 'moudle'}
            })
            .success(function (response) {
                $scope.moudle = response.entity;
            });

        $http.get("/common/list", {
                params: {_type: 'config', relateId: $scope.moudleId, type: 'moudle'}
            })
            .success(function (response) {
                $scope.configs = response.entities;
            });
        $http.get("/common/list", {
                params: {_type: 'cmdtemplate', relateId: $scope.moudleId, type: 'moudle'}
            })
            .success(function (response) {
                $scope.cmdTemplates = response.entities;
            });
        $scope.change_app = function () {
            $state.go('create_app', {appId: $scope.appId});
        };

        $scope.create_config = function () {
            $state.go('config_create', {relateId: $scope.moudleId, type: 'moudle'});
        };
        $scope.create_cmd_template = function () {
            $state.go('cmd_template_create', {relateId: $scope.moudleId, type: 'moudle'});
        };

    })
    .controller('config_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.config = {};
        $scope.config.relateId = $stateParams.relateId;
        $scope.config.type = $stateParams.type;
        $http.get("/configs/template")
            .success(function (response) {
                $scope.config.content = response.config;
            });
        $scope.create = function () {

            $http.post("/common/new", {_type: 'config', entity: $scope.config})
                .success(function (response) {
                    if ($stateParams.type == 'app')
                        $state.go('app_detail', {appId: $stateParams.relateId});
                    else
                        $state.go('moudle_detail', {id: $stateParams.relateId});
                });
        };
    })
    .controller('config_detailCtl', function ($scope, $http, $stateParams, $state) {
        var id = $stateParams.id;
        console.log($stateParams);
        $scope.config={};
        $scope.config.relateId = $stateParams.relateId;
        $scope.config.type = $stateParams.type;
        $http.get("/common/select", {
                params: {id: id, _type: 'config'}
            })
            .success(function (response) {
                $scope.config = response.entity;
            });


        $scope.create = function () {

            $http.post("/common/new", {_type: 'config', entity: $scope.config})
                .success(function (response) {
                    if ($stateParams.type == 'app')
                        $state.go('app_detail', {appId: $stateParams.relateId});
                    else
                        $state.go('moudle_detail', {id: $stateParams.relateId});
                });
        };
    })
    .controller('cmd_template_createCtl', function ($scope, $http, $stateParams, $state) {
        $scope.template = {};
        $scope.template.relateId = $stateParams.relateId;
        $scope.template.type = $stateParams.type;
        $scope.template.isDefault = false;
        if ($stateParams.id)
            $scope.template.id = $stateParams.id;
        if ($scope.template.id) {
            $http.get("/common/select", {
                    params: {id: $scope.template.id, _type: 'cmdtemplate'}
                })
                .success(function (response) {
                    $scope.template = response.entity;
                });
        }
        $scope.create = function () {

            $http.post("/common/new", {_type: 'cmdtemplate', entity: $scope.template})
                .success(function (response) {
                    if ($stateParams.type == 'moudle') {
                        $state.go('moudle_detail', {id: $stateParams.relateId});
                    } else
                        $state.go('app_detail', {appId: $stateParams.relateId});
                });
        };
    });

routeApp
    .controller('cmd_createCtl', function ($scope, $state, $stateParams, $http) {
        $scope.cmd = {};
        $scope.cmd.templateId = $stateParams.templateId;
        $scope.cmd.depends = '';
        if ($stateParams.id) {
            $scope.cmd.id = $stateParams.id;
            $http.get("/common/select", {
                    params: {id: $scope.cmd.id, _type: 'cmd'}
                })
                .success(function (response) {
                    $scope.cmd = response.entity;
                });
        }
        $scope.create = function () {
            $http.post("/common/new", {'_type': 'cmd', 'entity': $scope.cmd})
                .success(function (response) {
                    $state.go('cmd_template_detail', {id: $stateParams.templateId});
                });
        };
    })
    .controller('cmd_template_detailCtl', function ($scope, $state, $stateParams, $http) {
        var id = $stateParams.id;
        $http.get("/common/select", {
                params: {id: id, _type: 'cmdtemplate'}
            })
            .success(function (response) {
                $scope.template = response.entity;
            });
        $http.get("/common/list", {
                params: {templateId: id, _type: 'cmd'}
            })
            .success(function (response) {
                $scope.cmds = response.entities;
            });
        $scope.change_template = function () {
            $state.go('cmd_template_create', {
                relateId: $scope.template.relateId, type: $scope.template.type, id: $scope.template.id
            })
            ;
        };
        $scope.create_cmd = function () {
            $state.go('cmd_create', {
                templateId: $scope.template.id
            })
            ;
        };
    })
    .controller('pack_createCtl', function ($scope, $state, $stateParams, $http) {
        var appId = $stateParams.appId;

        $http.get("pack/loadInfos", {
                params: {appId: appId}
            })
            .success(function (response) {
                var result = response.infos;
                $scope.app = result.app;

                $scope.configs = result.configs;
                $scope.config = $scope.configs[0];

                $scope.templates = result.templates;
                $scope.template = $scope.templates[0];

                $scope.moudles = result.moudles;

                angular.forEach($scope.moudles, function (m, i, array) {
                    m.template = m.templates[0];
                });

            });


        $scope.create = function () {
            var data = {config: $scope.config, template: $scope.template, moudles: $scope.moudles, appId: appId}

            $http.post("/task/new", data)
                .success(function (response) {
                    $state.go('task_list');
                });
        };
    })
    .controller('task_listCtl', function ($scope, $state, $stateParams, $http) {

        $http.get("task/list")
            .success(function (response) {
                var tasks = response.tasks;
                $scope.tasks = tasks;

            });

    })
    .controller('step_listCtl', function ($scope, $state, $stateParams, $http) {
        var taskId = $stateParams.taskId;
        $http.get("/step/list", {params: {taskId: taskId}})
            .success(function (response) {
                var steps = response.steps;
                $scope.steps = steps;

            });

    });