function toggleCard(header) {
  const card = header.parentElement;
  card.classList.toggle('collapsed');

  // Меняем иконку стрелки
  const icon = header.querySelector('.toggle-icon');
  if (card.classList.contains('collapsed')) {
    icon.textContent = '►'; // или '▶'
  } else {
    icon.textContent = '▼'; // или '▼'
  }
}