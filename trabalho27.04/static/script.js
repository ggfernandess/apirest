
document.getElementById('vehicle-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const brand = document.getElementById('brand').value;
  const model = document.getElementById('model').value;
  const year = document.getElementById('year').value;

  fetch('/api/vehicles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand, model, year })
  })
  .then(() => loadVehicles());
});

function loadVehicles() {
  fetch('/api/vehicles')
    .then(response => response.json())
    .then(vehicles => {
      const list = document.getElementById('vehicle-list');
      list.innerHTML = '';
      vehicles.forEach(v => {
        const li = document.createElement('li');
        li.textContent = `${v.brand} ${v.model} - ${v.year}`;
        const del = document.createElement('button');
        del.textContent = 'Remover';
        del.onclick = () => {
          fetch(`/api/vehicles/${v.id}`, { method: 'DELETE' })
            .then(() => loadVehicles());
        };
        li.appendChild(del);
        list.appendChild(li);
      });
    });
}

loadVehicles();
