document.onload = function() {
    console.log('Document has loaded.');
}

var app = angular.module("chat_app", []);
app.controller("chat_controller", function($scope, $http) {
    console.log('Angular JS Working');
    $scope.counters = [];
    $scope.display_counters = []; // ['Bye bye world'];
    $scope.tweets = '';
    $scope.feature_type = '1';
    $scope.counters_2 = [];
    $scope.display_counters_2 = []; // ['Bye bye world'];
    $scope.tweets_2 = '';

    $scope.left_toggle = function(index) {
        console.log($scope.counters);
        console.log("Left Toggle", index, $scope.counters[index].Google);
        var current_display = $scope.counters[index].current_display;
        current_display = current_display - 1;
        if (current_display < 0) {
            current_display = $scope.counters[index].Google.length - 1;
        }
        // current_display = Math.abs(current_display-1)%$scope.counters[index].Google.length;
        $scope.counters[index].current_display = current_display;
        $scope.display_counters[index].Google = $scope.counters[index].Google[current_display];
        console.log($scope.counters);
    }
    $scope.right_toggle = function(index) {
        console.log("Right Toggle", index, $scope.counters[index].Google.length);
        var current_display = $scope.counters[index].current_display;
        current_display = Math.abs(current_display + 1) % $scope.counters[index].Google.length;
        $scope.counters[index].current_display = current_display;
        $scope.display_counters[index].Google = $scope.counters[index].Google[current_display];
    }
    $scope.showTweets = function(index) {
        console.log('Asked for tweets of: ', index, ', -- ', $scope.counters[index].Twitter);
        $scope.tweets = $scope.counters[index].Twitter; //.join('\n').toString();
    }
    $scope.left_toggle_2 = function(index) {
        console.log($scope.counters_2);
        console.log("Left Toggle", index, $scope.counters_2[index].Google.length);
        var current_display = $scope.counters_2[index].current_display;
        current_display = current_display - 1;
        if (current_display < 0) {
            current_display = $scope.counters_2[index].Google.length - 1;
        }
        // current_display = Math.abs(current_display-1)%$scope.counters[index].Google.length;
        $scope.counters_2[index].current_display = current_display;
        $scope.display_counters_2[index].Google = $scope.counters_2[index].Google[current_display];
        console.log($scope.counters_2);
    }
    $scope.right_toggle_2 = function(index) {
        console.log("Right Toggle", index, $scope.counters_2[index].Google.length);
        var current_display = $scope.counters_2[index].current_display;
        current_display = Math.abs(current_display + 1) % $scope.counters_2[index].Google.length;
        $scope.counters_2[index].current_display = current_display;
        $scope.display_counters_2[index].Google = $scope.counters_2[index].Google[current_display];
    }
    $scope.showTweets_2 = function(index) {
        console.log('Asked for tweets of: ', index, ', -- ', $scope.counters_2[index].Twitter);
        $scope.tweets_2 = $scope.counters_2[index].Twitter; //.join('\n').toString();
    }

    $scope.search = function() {
        if ($scope.feature_type.toString() == '1') {
            console.log('hoho');
            var getUrl = "http://localhost:5000/debate?query=";
            if ($scope.feature_type == 2) {
                getUrl = "http://localhost:5000/quick_info?query=";
            } else if ($scope.feature_type == 3) {
                getUrl = "http://localhost:5000/meaning?query=";
            }
            console.log($scope.raw_query);
            /*if (typeof $scope.raw_query == "string") {
                $scope.counters.pop();
                $scope.counters.push($scope.raw_query);
                $scope.display_counters.push($scope.raw_query);
            }*/
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
            $http.get(getUrl + encodeURI($scope.raw_query))
                .then(function mySuccess(response) {
                    console.log('Recieved...', response.data);
                    /*for(var counter in response.data) {
                        $scope.counters.push(response.data[counter]);
                    }*/
                    $scope.counters.push({
                        Google: response.data.results.Google,
                        Twitter: response.data.results.Twitter,
                        current_display: 0,
                        confidence: response.data.confidence
                    });
                    var temp = $scope.counters[$scope.counters.length-1].Google[$scope.counters[$scope.counters.length-1].Google.length-1].text.split('-ang-');//[$scope.counters.Google.length-1].split('-ang-');
                    console.log('Haha temp: ', temp);
                    $scope.counters[$scope.counters.length-1].Google[$scope.counters[$scope.counters.length-1].Google.length-1].text = temp.join('<br />');
                    //for(var chat in $scope.counters) {
                    $scope.display_counters.push({
                        Google: $scope.counters[$scope.counters.length - 1].Google[$scope.counters[$scope.counters.length - 1].current_display],
                        confidence: $scope.counters[$scope.counters.length - 1].confidence
                    });
                    // }
                    console.log($scope.counters, $scope.display_counters);
                }, function myError(response) {
                    console.log('Error!!', response);
                });
        }
    }
    $scope.search_2 = function() {
        console.log('haha');
        getUrl = "http://localhost:5000/quick_info?query=";
        console.log($scope.raw_query);
        $scope.counters_2.push($scope.raw_query);
        /*if (typeof $scope.raw_query == "string") {
            $scope.counters.pop();
            $scope.counters.push($scope.raw_query);
            $scope.display_counters_2.push($scope.raw_query);
        }*/
        $scope.counters.push($scope.raw_query);
        $scope.display_counters_2.push($scope.raw_query);
        var config = {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                }
            }
            /*$http.post("http://localhost:5000/debate", JSON.stringify({
                query: $scope.raw_query_2
            })).then(function mySuccess(response) {
                    console.log('Response: ', response);
                    $scope.myWelcome_2 = response.data;
                }, function myError(response) {
                    $scope.myWelcome_2 = response.statusText;
                });*/
        $http.get(getUrl + encodeURI($scope.raw_query))
            .then(function mySuccess(response) {
                console.log('Recieved...', response.data);
                /*for(var counter in response.data) {
                    $scope.counters_2.push(response.data[counter]);
                }*/
                $scope.counters_2.push({
                    Google: response.data.results.Google,
                    Twitter: response.data.results.Twitter,
                    current_display: 0,
                    confidence: response.data.confidence
                });
                var temp = $scope.counters[$scope.counters.length-1].Google[$scope.counters[$scope.counters.length-1].Google.length-1].text.split('-ang-');//[$scope.counters.Google.length-1].split('-ang-');
                console.log('Haha temp: ', temp);
                $scope.counters[$scope.counters.length-1].Google[$scope.counters[$scope.counters.length-1].Google.length-1].text = temp.join('<br />');
                //for(var chat in $scope.counters_2) {
                $scope.display_counters_2.push({
                    Google: $scope.counters_2[$scope.counters_2.length - 1].Google[$scope.counters_2[$scope.counters_2.length - 1].current_display],
                    confidence: $scope.counters_2[$scope.counters_2.length - 1].confidence
                });
                // }
                console.log($scope.counters_2, $scope.display_counters_2);
            }, function myError(response) {
                console.log('Error!!', response);
            });
    }
});