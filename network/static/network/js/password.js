// Toggle Password Visibility
document.querySelector('.toggle-password').addEventListener('click', function () {
  const passwordField = document.getElementById('password');
  const passwordFieldType = passwordField.getAttribute('type');
  if (passwordFieldType === 'password') {
      passwordField.setAttribute('type', 'text');
      this.textContent = 'Hide';
  } else {
      passwordField.setAttribute('type', 'password');
      this.textContent = 'Show';
  }
});
