document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('loginForm');
    if(loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Here, you would validate credentials and potentially make an API call
            // For demonstration, we'll just log the username and redirect
            var username = loginForm.querySelector('[name="username"]').value;
            console.log('Logging in', username);
            // Redirect to the dashboard
            window.location.href = 'dashboard.html';
        });
    }
});