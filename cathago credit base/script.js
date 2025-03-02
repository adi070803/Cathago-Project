function login() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    
    fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('user-name').innerText = username;
        } else {
            alert('Login failed');
        }
    });
}

function register() {
    let username = document.getElementById('reg-username').value;
    let password = document.getElementById('reg-password').value;
    
    fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}
