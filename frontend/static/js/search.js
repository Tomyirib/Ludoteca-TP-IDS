async function get_data() {
  const url = "http://localhost:8080/games/get_names";
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

  for (let i = 0; i < data.length; i++) {
    const juego = data[i][0];

    if (juego.toLowerCase().includes(text.toLowerCase())) {
      const link = document.createElement("a");
      link.href = `/juego/${data[i][1]}`; 
      link.textContent = juego;
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