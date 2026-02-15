// Client-side form validation
function validateRegisterForm() {
    let password = document.getElementById('password').value;
    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }
    return true;
}

function validateLoginForm() {
    // Simple check – can be extended
    return true;
}

function validatePostForm() {
    let title = document.getElementById('title').value.trim();
    let content = document.getElementById('content').value.trim();
    if (title === '' || content === '') {
        alert('Title and content cannot be empty.');
        return false;
    }
    return true;
}