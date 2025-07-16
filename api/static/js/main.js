// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtener el botón por su ID
    const botonSaludo = document.getElementById('saludo');
    
    // Agregar un evento de clic al botón
    botonSaludo.addEventListener('click', function() {
        // Mostrar un mensaje de alerta cuando se hace clic en el botón
        alert('¡Hola! Gracias por visitar mi aplicación Flask en Vercel.');
        
        // Cambiar el texto del botón temporalmente
        const textoOriginal = botonSaludo.textContent;
        botonSaludo.textContent = '¡Gracias por hacer clic!';
        
        // Restaurar el texto original después de 2 segundos
        setTimeout(function() {
            botonSaludo.textContent = textoOriginal;
        }, 2000);
    });
    
    // Efecto de carga suave
    document.body.style.opacity = '0';
    setTimeout(function() {
        document.body.style.transition = 'opacity 1s';
        document.body.style.opacity = '1';
    }, 100);
});
