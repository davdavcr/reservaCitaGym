document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("password-toggle");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("change", function () {
        if (togglePassword.checked) {
            passwordField.type = "text";
        } else {
            passwordField.type = "password";
        }
    });
});
