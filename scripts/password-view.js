const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const togglePassword = document.getElementById('togglePassword');

togglePassword.addEventListener('click', function () {
    // Nos basamos en el estado del primer input para decidir el cambio
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    
    // Se lo aplicamos a los dos por igual
    passwordInput.setAttribute('type', type);
    confirmPasswordInput.setAttribute('type', type);
    
    // Cambiamos el emoji
    this.textContent = type === 'password' ? '👁️' : '🙈';
});