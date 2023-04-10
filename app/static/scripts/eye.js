/**
 * Initialize a password and confirm password field with visibility toggling functionality.
 * @param {string} passwordFieldId - The ID of the password field.
 * @param {string} confirmPasswordFieldId - The ID of the confirm password field (optional).
 */
function initTogglePassword(passwordFieldId, confirmPasswordFieldId) {
    // Get the toggle password button and the password field
    const togglePassword = document.getElementById('toggle-password');
    const password = document.getElementById(passwordFieldId);
    let passwordVisible = false;
    // Add a click event listener to the toggle password button
    togglePassword.addEventListener('click', function () {
        // Toggle the password visibility and update the password field type and button text
        passwordVisible = !passwordVisible;
        password.type = passwordVisible ? 'text' : 'password';
        togglePassword.textContent = passwordVisible ? '🙈' : '👁';
    });
    // If a confirm password field ID is provided
    if (confirmPasswordFieldId) {
        // Get the toggle confirm password button and the confirm password field
        const toggleConfirmPassword = document.getElementById('toggle-confirm-password');
        const confirmPassword = document.getElementById(confirmPasswordFieldId);
        let confirmPasswordVisible = false;
        // Add a click event listener to the toggle confirm password button
        toggleConfirmPassword.addEventListener('click', function () {
             // Toggle the confirm password visibility and update the confirm password field type and button text
            confirmPasswordVisible = !confirmPasswordVisible;
            confirmPassword.type = confirmPasswordVisible ? 'text' : 'password';
            toggleConfirmPassword.textContent = confirmPasswordVisible ? '🙈' : '👁';
        });
    }
}
