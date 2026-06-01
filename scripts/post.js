const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

const form = document.getElementById("postForm");
const input = document.getElementById("postText");
const counter = document.getElementById("counter");
const status = document.getElementById("status");

// contador de caracteres
input.addEventListener("input", () => {
    counter.innerText = `${input.value.length} / 50`;
});

function sanitize(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;").trim();
}

// crear post
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = sanitize(input.value);

    if (text.length === 0) {
        alert("No puedes publicar vacío");
        return;
    }

    if (text.length > 50) {
        alert("Máximo 50 caracteres");
        return;
    }

    // usuario logueado
    const { data: { user } } = await client.auth.getUser();

    if (!user) {
        alert("Debes iniciar sesión");
        return;
    }

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

    status.innerText = "✅ Post publicado";
    input.value = "";
    counter.innerText = "0 / 50";
});