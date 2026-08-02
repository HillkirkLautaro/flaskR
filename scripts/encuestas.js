const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";
const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

let lastSubmit = 0;
const form = document.getElementById("encuestaForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // 1. Anti-spam de UI
    if (Date.now() - lastSubmit < 5000) {
        alert("Espera 5 segundos antes de enviar otra encuesta");
        return;
    }

    // 2. Obtener valores sin sanitizar innecesariamente al guardar
    const pregunta = document.getElementById("Pregunta").value.trim();
    const opcion1 = document.getElementById("Opcion1").value.trim();
    const opcion2 = document.getElementById("Opcion2").value.trim();

    // 3. Validaciones básicas en cliente
    if (pregunta.length < 5) {
        alert("La pregunta debe tener al menos 5 caracteres");
        return;
    }

    if (opcion1 === opcion2) {
        alert("Las opciones no pueden ser iguales");
        return;
    }

    lastSubmit = Date.now();

    // 4. Inserción en Supabase
    const { error } = await client
        .from("Encuesta")
        .insert([{ Pregunta: pregunta, Opcion1: opcion1, Opcion2: opcion2 }]);

    if (error) {
        console.error("Error al insertar:", error);
        alert("No se pudo crear la encuesta: " + error.message);
        return;
    }

    alert("Encuesta creada correctamente");
    form.reset();
});
