const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

let lastSubmit = 0;

function sanitize(input) {
    return input.replace(/</g, "&lt;").replace(/>/g, "&gt;").trim();
}

const form = document.getElementById("registroForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // anti spam
    if (Date.now() - lastSubmit < 5000) {
        alert("Espera 5 segundos antes de registrarte otra vez");
        return;
    }
    lastSubmit = Date.now();

    const username = sanitize(document.getElementById("username").value);
    const email = sanitize(document.getElementById("email").value);
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const captchaToken = hcaptcha.getResponse();

    if (!captchaToken) {
        alert("Completa el captcha");
        return;
    }

    if (password !== confirmPassword) {
        alert("Las contraseñas no coinciden");
        return;
    }

    if (username.length < 3) {
        alert("Usuario muy corto");
        return;
    }

    // AUTH con captcha
    const { data, error } = await client.auth.signUp({
        email: email,
        password: password,
        options: {
            captchaToken: captchaToken
        }
    });

    if (error) {
        console.error(error);
        alert("Error auth: " + error.message);
        return;
    }

    const userId = data.user.id;

    // profile
    const { error: profileError } = await client
        .from("profiles")
        .insert([
            {
                id: userId,
                username: username
            }
        ]);

    if (profileError) {
        console.error(profileError);
        alert("Usuario creado pero error en perfil");
        return;
    }

    alert("Usuario registrado correctamente");
    form.reset();
    hcaptcha.reset();
});