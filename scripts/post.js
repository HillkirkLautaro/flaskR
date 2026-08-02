const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";
const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

const form = document.getElementById("postForm");
const input = document.getElementById("postText");
const counter = document.getElementById("counter");
const status = document.getElementById("status");
const submitBtn = form.querySelector('button[type="submit"]');

// ==========================
// 🔐 VERIFICAR SESIÓN
// ==========================
async function getUser() {
    const { data: { user }, error } = await client.auth.getUser();

    if (error || !user) {
        window.location.href = "login.html";
        return null;
    }

    return user;
}

// ==========================
// 📊 CONTADOR EN TIEMPO REAL
// ==========================
input.addEventListener("input", () => {
    const length = input.value.trim().length;
    counter.innerText = `${length} / 50`;
    
    if (length > 50) {
        counter.style.color = "red";
    } else {
        counter.style.color = "inherit";
    }
});

// ==========================
// 🚀 PUBLICAR POST
// ==========================
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const user = await getUser();
    if (!user) return;

    // 1. Obtener texto plano (sin sanitizar para la BD)
    const rawText = input.value.trim();

    // 2. Validaciones básicas
    if (!rawText) {
        alert("No puedes publicar un mensaje vacío");
        return;
    }

    if (rawText.length > 50) {
        alert("El post no puede superar los 50 caracteres");
        return;
    }

    // 3. Obtener token de hCaptcha
    const captchaToken = window.hcaptcha?.getResponse?.();
    if (!captchaToken) {
        alert("Por favor, completa el captcha");
        return;
    }

    // 4. Bloquear botón para evitar doble envío (Anti-spam UI)
    if (submitBtn) submitBtn.disabled = true;
    status.innerText = "Publicando...";

    // 5. Inserción segura enviando el captchaToken en las opciones
    const { error } = await client
        .from("posts")
        .insert(
            [
                {
                    user_id: user.id,
                    content: rawText // Guardamos texto nativo
                }
            ],
            { captchaToken }
        );

    // Recompone el estado del botón
    if (submitBtn) submitBtn.disabled = false;

    if (error) {
        console.error("Error al insertar post:", error);
        status.innerText = "❌ Error al publicar: " + error.message;
        if (window.hcaptcha) window.hcaptcha.reset();
        return;
    }

    // 6. Éxito
    status.innerText = "✅ Post publicado correctamente";
    input.value = "";
    counter.innerText = "0 / 50";
    if (window.hcaptcha) window.hcaptcha.reset();
});
