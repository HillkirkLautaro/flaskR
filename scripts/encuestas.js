const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(
    supabaseUrl,
    supabaseKey
);

// anti spam
let lastSubmit = 0;

function sanitize(input) {
    return input.replace(/</g, "&lt;").replace(/>/g, "&gt;").trim();
}

const form = document.getElementById("encuestaForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (Date.now() - lastSubmit < 5000) {
        alert("Espera 5 segundos antes de enviar otra encuesta");
        return;
    }
    lastSubmit = Date.now();

    const pregunta = sanitize(document.getElementById("Pregunta").value);
    const opcion1 = sanitize(document.getElementById("Opcion1").value);
    const opcion2 = sanitize(document.getElementById("Opcion2").value);

    if (pregunta.length < 5) {
        alert("Pregunta muy corta");
        return;
    }

    if (opcion1 === opcion2) {
        alert("Opciones iguales no válidas");
        return;
    }

    const { error } = await client
        .from("Encuesta")
        .insert([
            {
                Pregunta: pregunta,
                Opcion1: opcion1,
                Opcion2: opcion2
            }
        ]);

    if (error) {
        console.error(error);
        alert(error.message);
        return;
    }

    alert("Encuesta creada correctamente");
    form.reset();
});