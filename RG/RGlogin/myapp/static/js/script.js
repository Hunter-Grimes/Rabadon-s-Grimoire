// JavaScript to handle login form submission
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var username = this.elements['username'].value;
    var password = this.elements['password'].value;
    // Simulate login process (replace with actual authentication logic)
    if (username === 'your_username' && password === 'your_password') {
        // Hide login section
        document.getElementById('login-section').style.display = 'none';
        // Show welcome message with username
        document.getElementById('welcome-section').style.display = 'block';
        document.getElementById('welcome-message').textContent = 'Welcome, ' + username + '!';
    } else {
        alert('Invalid username or password');
    }
});