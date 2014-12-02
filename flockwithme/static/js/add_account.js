$(function() {
    OAuth.initialize('AJNxVaMg67eYFkejUcYJRHcudTA');

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