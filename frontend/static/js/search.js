async function get_data() {
  const url = "http://localhost:8080/games";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(error.message);
  }
}

function search_games(data, text) {
  const contenedor = document.getElementById("resultados");
  contenedor.innerHTML = ""; 

  for (let i = 0; i < data.games.length; i++) {
    const juego = data.games[i];

    if (juego.name.toLowerCase().includes(text.toLowerCase())) {
      const link = document.createElement("a");
      link.href = `/juego/${juego.id}`; 
      link.textContent = juego.name;
      link.style.display = "block";
      link.style.marginLeft = "2vh";
      contenedor.appendChild(link);
    }
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const input = document.getElementById("search");
  const data = await get_data();

  input.addEventListener('input', () => {
    const text = input.value.trim();
    search_games(data, text);
  });
});