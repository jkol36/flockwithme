$(function() {
    OAuth.initialize('4zofYmuzWczQY0QGZ8Ix4M-UEHM');

    $('#associate-button').click(function() {
        OAuth.popup('twitter', function(err, result) {
            console.log(result);
            if (err) {
                console.log(err);
                return;
            }
            result.me().done(function(me) {
                ajaxPost('/profile/ajax/add_account/', {
                    'provider': 'twitter',
                    'token': result.oauth_token,
                    'secret': result.oauth_token_secret,
                    'handle': me.alias
                }, function(data) {
                    location.reload();
                });
            });
        });
    });
})