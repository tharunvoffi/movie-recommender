async function getRecommendations() {
  const title = document.getElementById("movieInput").value;
  const semanticDiv = document.getElementById("semanticResults");
  const genreDiv = document.getElementById("genreResults");
  const loader = document.getElementById("loader");
  const resultsSection = document.getElementById("resultsSection");

  semanticDiv.innerHTML = "";
  genreDiv.innerHTML = "";
  loader.style.display = "block";

  const res = await fetch("/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });

  const data = await res.json();
  loader.style.display = "none";

  if (data.error) {
    semanticDiv.innerHTML = `<p>${data.error}</p>`;
    resultsSection.style.display = "block";
    return;
  }

  resultsSection.style.display = "block";

  if (data.suggestion) {
    semanticDiv.innerHTML += `<p>Did you mean <b>${data.suggestion}</b>?</p>`;
  }

  data.semantic.forEach((movie, i) => {
    semanticDiv.innerHTML += `<div class="movie">${i + 1}. ${movie}</div>`;
  });

  data.genre.forEach((movie, i) => {
    genreDiv.innerHTML += `<div class="movie">${i + 1}. ${movie}</div>`;
  });
}
