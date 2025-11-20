/* global alert */

/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const logoutLink = document.getElementById('logout-link');

  if (logoutLink) logoutLink.addEventListener('click', logoutUser);

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }

  const placesList = document.getElementById('places-list');
  if (placesList) checkAuthentication();

  /* -----------------------------------------------------------
     PRICE FILTER → populate dynamically + filtering
  ----------------------------------------------------------- */
  const priceFilter = document.getElementById('price-filter');

  if (priceFilter) {
    // Inject Holberton-required options
    priceFilter.innerHTML = `
      <option value="All">All</option>
      <option value="10">10 €</option>
      <option value="50">50 €</option>
      <option value="100">100 €</option>
    `;

    priceFilter.addEventListener('change', (event) => {
      const selected = event.target.value;
      const cards = document.querySelectorAll('.place-card');

      cards.forEach((card) => {
        const price = parseFloat(card.dataset.price);

        if (selected === 'All') {
          card.style.display = '';
        } else {
          const max = parseFloat(selected);
          card.style.display = price <= max ? '' : 'none';
        }
      });
    });
  }
});

/* ---------------- LOGIN ---------------- */
async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

/* ---------------- AUTH CHECK ---------------- */
function checkAuthentication() {
  const token = getCookie('token');

  const headerLogin = document.getElementById('login-link');
  const navLogin = document.getElementById('nav-login');
  const logoutLink = document.getElementById('logout-link');

  if (!token) {
    headerLogin.style.display = 'block';
    navLogin.style.display = 'block';
    logoutLink.style.display = 'none';
  } else {
    headerLogin.style.display = 'none';
    navLogin.style.display = 'none';
    logoutLink.style.display = 'block';

    fetchPlaces(token);
  }
}

/* ---------------- COOKIE READER ---------------- */
function getCookie(name) {
  const cookies = document.cookie.split(';');

  for (const cookie of cookies) {
    const c = cookie.trim();
    const parts = c.split('=');
    if (parts[0] === name) return parts[1];
  }
  return null;
}

/* ---------------- FETCH PLACES ---------------- */
async function fetchPlaces(token) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });

  if (!response.ok) {
    alert('Failed to load places');
    return;
  }

  const places = await response.json();
  displayPlaces(places);
}

/* ---------------- DISPLAY PLACES ---------------- */
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  list.innerHTML = '';

  for (const place of places) {
    const div = document.createElement('div');
    div.classList.add('place-card');

    div.dataset.price = place.price;

    div.innerHTML = `
      <img src="https://placehold.co/400x250?text=${encodeURIComponent(place.title)}" alt="Place image">
      <div class="place-card-content">
        <h3>${place.title}</h3>
        <p><strong>Price:</strong> ${place.price} €</p>
        <p><strong>Latitude:</strong> ${place.latitude}</p>
        <p><strong>Longitude:</strong> ${place.longitude}</p>
        <a class="details-button" href="#">Details</a>
      </div>
    `;

    list.appendChild(div);
  }
}

/* ---------------- LOGOUT ---------------- */
function logoutUser() {
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  window.location.reload();
}
