document.onload = function() {
    console.log('Document has loaded.');
}

var app = angular.module("chat_app", []);
app.controller("chat_controller", function($scope, $http) {
    /*var socket = io('http://localhost:50007');
    // socket.connect();
    socket.open();
    socket.on('connection', function() {
    	console.log('Connection established...');
    });*/

    console.log('Hello World haha');
    $scope.firstName = 'Nirabhra';
    $scope.lastName = 'Tapaswi';
    $scope.names = [1, 2, 3, 4, 5];
    $scope.counters = ['haha', 'hello'];
    $scope.array = [1, 2, 3, 4, 5];

    $scope.search = function() {
        console.log($scope.raw_query);
        var config = {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
            }
        }
        /*$http.post("http://localhost:5000/debate", JSON.stringify({
        	query: $scope.raw_query
        })).then(function mySuccess(response) {
                console.log('Response: ', response);
                $scope.myWelcome = response.data;
            }, function myError(response) {
                $scope.myWelcome = response.statusText;
            });*/
        $http.get("http://localhost:5000/debate?query="+encodeURI($scope.raw_query))
            .then(function mySuccess(response) {
                console.log('Recieved...', response.data);
                for(var counter in response.data) {
                    $scope.counters.push(response.data[counter]);
                }
                console.log($scope.counters);
                $scope.firstName = "Null"
            }, function myError(response) {
                console.log('Error!!');
            })
    }
});