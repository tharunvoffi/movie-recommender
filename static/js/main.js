document.addEventListener("DOMContentLoaded", () => {

  const input = document.getElementById("movieInput");
  if (!input) return; // ✅ prevents errors on Home/About

  const semantic = document.getElementById("semantic");
  const genre = document.getElementById("genre");
  const ai = document.getElementById("aiMessage");
  const results = document.getElementById("results");

  /* 🔑 ENTER KEY SUPPORT */
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      getRecommendations();
    }
  });

  window.getRecommendations = async function () {
    const title = input.value.trim();
    if (!title) return;

    semantic.innerHTML = "";
    genre.innerHTML = "";
    ai.innerHTML = "";
    results.style.display = "block";

    try {
      const res = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      });

      const data = await res.json();

      if (data.error) {
        ai.innerHTML = `<div class="ai">${data.error}</div>`;
        return;
      }

      if (data.suggestion) {
        ai.innerHTML = `<div class="ai">Showing results for ${data.suggestion}</div>`;
      }

      data.semantic.forEach(movie => {
        semantic.innerHTML += `<div class="movie-card">${movie}</div>`;
      });

      data.genre.forEach(movie => {
        genre.innerHTML += `<div class="movie-card">${movie}</div>`;
      });

    } catch (err) {
      ai.innerHTML = `<div class="ai">Something went wrong</div>`;
      console.error(err);
    }
  };
});
