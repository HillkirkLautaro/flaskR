const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

const form = document.getElementById("postForm");
const input = document.getElementById("postText");
const counter = document.getElementById("counter");
const status = document.getElementById("status");

// ==========================
// 🔐 PROTEGER FUNCIONALIDAD (como profile.js)
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
// ✍️ SANITIZE
// ==========================
function sanitize(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;").trim();
}

// ==========================
// 📊 CONTADOR
// ==========================
input.addEventListener("input", () => {
    counter.innerText = `${input.value.length} / 50`;
});

// ==========================
// 🚀 SUBMIT POST
// ==========================
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const user = await getUser();
    if (!user) return;

    const text = sanitize(input.value);

    // 🔴 VALIDACIONES
    if (!text) {
        alert("No puedes publicar vacío");
        return;
    }

    if (text.length > 50) {
        alert("Máximo 50 caracteres");
        return;
    }

    // ==========================
    // 🤖 CAPTCHA (MISMA LÓGICA SIMPLE)
    // ==========================
    const captchaToken = hcaptcha.getResponse();

    if (!captchaToken) {
        alert("Completa el captcha");
        return;
    }

    // ==========================
    // 💾 INSERT POST
    // ==========================
    const { error } = await client
        .from("posts")
        .insert([
            {
                user_id: user.id,
                content: text
            }
        ]);

    if (error) {
        console.error(error);
        status.innerText = "❌ Error al publicar";
        return;
    }

    // ==========================
    // ✅ SUCCESS STATE
    // ==========================
    status.innerText = "✅ Post publicado";
    input.value = "";
    counter.innerText = "0 / 50";

    hcaptcha.reset();
});