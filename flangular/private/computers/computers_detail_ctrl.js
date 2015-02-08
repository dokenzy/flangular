angular.module('computers.detail', [])
.controller('ComputersDetailCtrl', [
             '$scope','$state','$stateParams','instance',
    function ($scope,  $state,  $stateParams,  instance) {
        $scope.model = instance('computer');
        $scope.model.$select($stateParams._id);

        $scope.create = function() {
            $state.go('computers.detail', {_id: -1});
        };

        $scope.save = function() {
            $scope.model.$save().then(function() {
                console.log('DONE', $scope.model._id.$oid);
                var _id = {$oid: $scope.model._id.$oid};
                $state.go('computers.detail', {_id: _id.$oid});
            });
        };

        $scope.remove = function() {
            $scope.model.$remove().then(function() {
                $state.go('computers.list');
            });
        };
    }
]);
