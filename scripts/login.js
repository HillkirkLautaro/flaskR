const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

let lastSubmit = 0;

const form = document.getElementById("loginForm");
const status = document.getElementById("status");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (Date.now() - lastSubmit < 5000) {
        alert("Espera 5 segundos antes de volver a intentar");
        return;
    }
    lastSubmit = Date.now();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // captcha opcional (si lo querés exigir en login)
    const captchaToken = window.hcaptcha?.getResponse?.();

    const { data, error } = await client.auth.signInWithPassword({
        email: email,
        password: password,
        options: captchaToken
            ? { captchaToken }
            : undefined
    });

    if (error) {
        console.error(error);
        status.innerText = "❌ Error: " + error.message;
        return;
    }

    status.innerText = "✅ Login exitoso";

    // guardar sesión
    localStorage.setItem("session", JSON.stringify(data.session));

    setTimeout(() => {
        window.location.href = "index.html";
    }, 1000);
});