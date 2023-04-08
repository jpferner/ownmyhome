function initTogglePassword(passwordFieldId, confirmPasswordFieldId) {
    const togglePassword = document.getElementById('toggle-password');
    const password = document.getElementById(passwordFieldId);
    let passwordVisible = false;

    togglePassword.addEventListener('click', function () {
        passwordVisible = !passwordVisible;
        password.type = passwordVisible ? 'text' : 'password';
        togglePassword.textContent = passwordVisible ? '🙈' : '👁';
    });

    if (confirmPasswordFieldId) {
        const toggleConfirmPassword = document.getElementById('toggle-confirm-password');
        const confirmPassword = document.getElementById(confirmPasswordFieldId);
        let confirmPasswordVisible = false;

        toggleConfirmPassword.addEventListener('click', function () {
            confirmPasswordVisible = !confirmPasswordVisible;
            confirmPassword.type = confirmPasswordVisible ? 'text' : 'password';
            toggleConfirmPassword.textContent = confirmPasswordVisible ? '🙈' : '👁';
        });
    }
}
