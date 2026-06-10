const supabaseKey = "sb_publishable_ut3DRPMELPw-6nCvxSbMjA_Cttmj4FA";
const supabaseUrl = "https://ftbyjjmvflxlotnkauwd.supabase.co";

const client = window.supabase.createClient(supabaseUrl, supabaseKey);

const container = document.getElementById("postsContainer");

function sanitize(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
let page = 0;
const POSTS_PER_PAGE = 3;
let maxPageReached = false;

async function loadPosts() {

    const from = page * POSTS_PER_PAGE;
    const to = from + POSTS_PER_PAGE - 1;

    const { data, error } = await client
  .from("posts")
  .select(`
      id,
      content,
      created_at,
      profiles(username)
  `)
  .order("created_at", { ascending: false })
  .range(from, to);

    if (error) {
        console.error(error);
        container.innerHTML = "<p>Error cargando posts</p>";
        return;
    }

    if (!data || data.length === 0) {
        container.innerHTML = "<p>No hay posts todavía</p>";
        return;
    }
    if (!data || data.length === 0) {
        maxPageReached = true;
        return;
    }

    maxPageReached = false;

    container.innerHTML = "";

    data.forEach(post => {

        const div = document.createElement("div");
        div.className = "post-card";

        div.innerHTML = `
            <p><strong>User:</strong> ${post.profiles?.username}</p>
            <p>${sanitize(post.content)}</p>
            <small>${new Date(post.created_at).toLocaleString()}</small>
            <hr>
        `;
    
        container.appendChild(div);
    });
    if (data.length < POSTS_PER_PAGE) {
    document.getElementById("loadMoreBtn").style.display = "none";
}}

document.getElementById("loadMoreBtn").addEventListener("click", async () => {

    page++;

    const success = await loadPosts();

    if (!success) {
        page--;
    }
});
document.getElementById("loadMinusBtn").addEventListener("click", () => {
    if (page > 0) {
        page--;
        loadPosts();
    }
});
loadPosts();
