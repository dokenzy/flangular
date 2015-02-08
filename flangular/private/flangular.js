angular.module('flangular', [
    'ui.router',
    'ui.bootstrap',
    'computers'
])
.provider('collection', function() {
    var baseUrl = '';

    this.setBaseUrl = function(url) {
        baseUrl = url;
    };

    this.$get = ['$http', function($http) {
        var Collection = function(modelUrl) {
            this._modelUrl = baseUrl + modelUrl;
        };

        (function() {
            var that = this;
            this.objects = [];
            this.count = 0;

            this.load = function() {
                $http.get(this._modelUrl, {
                    params: {
                        page: this.currentPage
                    }
                }).then(function(resp) {
                    var d = resp.data;
                    that.objects = d.objects;
                    that.count = d.count;
                }, function(err) {
                    console.log('failed to load model', err);
                });
            };

        }).call(Collection.prototype);

        return function(modelUrl) {
            return new Collection(modelUrl);
        };
    }];
})
.provider('instance', function() {
    var baseUrl = '';

    this.setBaseUrl = function(url) {
        baseUrl = url;
    };

    this.$get = ['$http', '$q', function($http, $q) {
        var Instance = function(modelUrl) {
            this._modelUrl = baseUrl + modelUrl;
            this._id = -1;
        };

        (function() {
            this.$select = function(id) {
                var that = this;

                if (!id || id < 0) {
                    return;
                }

                $http.get(this._modelUrl + '/' + id).then(function(resp) {
                    var d = resp.data;
                    for (var key in d) {
                        if (d.hasOwnProperty(key)) {
                            that[key] = d[key];
                        }
                    }
                }, function(err) {
                    console.log('failed to load model', err);
                });
            };

            this.$save = function() {
                var that = this;
                var data = {};
                for (var key in this) {
                    if (this.hasOwnProperty(key)) {// id? 
                        data[key] = this[key];
                    }
                }


                if (this._id !== -1 && this._id.$oid !== '') {
                    return $http.put(this._modelUrl + '/' + this._id.$oid, data);
                } else {
                    var deferred = $q.defer();
                    $http.post(this._modelUrl, data).then(function(resp) {
                        var data = JSON.parse(resp.data);
                        that._id = {};
                        that._id.$oid = data._id.$oid;
                        deferred.resolve();
                    }, deferred.reject);

                    return deferred.promise;
                }

            };

            this.$remove = function() {
                return $http.delete(this._modelUrl + '/' + this._id.$oid);
            };

        }).call(Instance.prototype);

        return function(instanceUrl) {
            return new Instance(instanceUrl);
        };
    }];
})
.config([
             '$stateProvider','collectionProvider','instanceProvider',
    function ($stateProvider,  collectionProvider,  instanceProvider) {
        $stateProvider.state('home', {
            url: "/",
            template: '<p>Flangular Demo App</p>'
        });

        collectionProvider.setBaseUrl('api/');
        instanceProvider.setBaseUrl('api/');
    }
  ]
)
.run(
  [         '$rootScope', '$state', '$stateParams',
    function($rootScope,   $state,   $stateParams) {

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    }
  ]
);
