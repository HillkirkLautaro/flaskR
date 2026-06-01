const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

const emailEl = document.getElementById("email");
const userIdEl = document.getElementById("userid");
const usernameEl = document.getElementById("username");
const status = document.getElementById("status");

// 🔐 PROTEGER PÁGINA
async function loadProfile() {

    const { data: { user }, error } = await client.auth.getUser();

    if (error || !user) {
        window.location.href = "login.html";
        return;
    }

    emailEl.innerText = user.email;
    userIdEl.innerText = user.id;

    // traer username desde profiles
    const { data, error: profileError } = await client
        .from("profiles")
        .select("username")
        .eq("id", user.id)
        .maybeSingle();

    if (!profileError && data) {
        usernameEl.innerText = data.username;
    } else {
        usernameEl.innerText = "No definido";
    }
}

loadProfile();

// 🚪 LOGOUT
document.getElementById("logoutBtn").addEventListener("click", async () => {

    const { error } = await client.auth.signOut();

    if (error) {
        status.innerText = "Error al cerrar sesión";
        return;
    }

    localStorage.removeItem("session");

    window.location.href = "login.html";
});