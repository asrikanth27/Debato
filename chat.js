document.onload = function() {
    console.log('Document has loaded.');
}

var app = angular.module("chat_app", []);
app.controller("chat_controller", function($scope, $http) {
    console.log('Angular JS Working');
    $scope.counters = [];
    $scope.display_counters = []; // ['Bye bye world'];
    $scope.tweets = '';

    $scope.left_toggle = function(self) {
        console.log("Left Toggle", self, $scope.counters[self].Google.length);
        var current_display = $scope.counters[self].current_display;
        current_display = current_display - 1;
        if (current_display<0) {
            current_display = $scope.counters[self].Google.length-1;
        }
        // current_display = Math.abs(current_display-1)%$scope.counters[self].Google.length;
        $scope.counters[self].current_display = current_display;
        $scope.display_counters[self] = $scope.counters[self].Google[current_display];
        console.log($scope.counters);
    }
    $scope.right_toggle = function(self) {
        console.log("Right Toggle", self, $scope.counters[self].Google.length);
        var current_display = $scope.counters[self].current_display;
        current_display = Math.abs(current_display+1)%$scope.counters[self].Google.length;
        $scope.counters[self].current_display = current_display;
        $scope.display_counters[self] = $scope.counters[self].Google[current_display];
    }
    $scope.showTweets = function(index) {
        console.log('Asked for tweets of: ', index, ', -- ', $scope.counters[index].Twitter);
        $scope.tweets = $scope.counters[index].Twitter;//.join('\n').toString();
    }

    $scope.search = function() {
        console.log($scope.raw_query);
        $scope.counters.push($scope.raw_query);
        $scope.display_counters.push($scope.raw_query);
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
        $http.get("http://localhost:5000/debate?query=" + encodeURI($scope.raw_query))
            .then(function mySuccess(response) {
                console.log('Recieved...', response.data);
                /*for(var counter in response.data) {
                    $scope.counters.push(response.data[counter]);
                }*/
                $scope.counters.push({
                    Google: response.data.Google,
                    Twitter: response.data.Twitter,
                    current_display: 0
                });
                //for(var chat in $scope.counters) {
                $scope.display_counters.push($scope.counters[$scope.counters.length - 1].Google[$scope.counters[$scope.counters.length - 1].current_display]);
                // }
                console.log($scope.counters);
            }, function myError(response) {
                console.log('Error!!', response);
            })
    }
});