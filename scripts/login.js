const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";
const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

let lastSubmit = 0;

const form = document.getElementById("loginForm");
const status = document.getElementById("status");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // 1. Rate-limiting local (UI)
    if (Date.now() - lastSubmit < 5000) {
        status.innerText = "⚠️ Espera 5 segundos antes de volver a intentar";
        return;
    }

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    // 2. Validar Captcha Obligatorio (Si lo activaste en Supabase Auth)
    const captchaToken = window.hcaptcha?.getResponse?.();
    if (!captchaToken) {
        status.innerText = "⚠️ Por favor, completa el Captcha";
        return;
    }

    lastSubmit = Date.now();
    status.innerText = "Cargando...";

    // 3. Inicio de sesión seguro con Supabase
    const { data, error } = await client.auth.signInWithPassword({
        email: email,
        password: password,
        options: { captchaToken }
    });

    if (error) {
        console.error("Error de autenticación:", error.message);
        // Mensaje genérico para evitar enumeración de correos
        status.innerText = "❌ Credenciales incorrectas o error de autenticación";
        if (window.hcaptcha) window.hcaptcha.reset(); // Resetear captcha tras fallo
        return;
    }

    status.innerText = "✅ Login exitoso. Redirigiendo...";

    // NO guardes la sesión en localStorage manualmente. Supabase ya lo hizo.

    setTimeout(() => {
        window.location.href = "index.html";
    }, 1000);
});
