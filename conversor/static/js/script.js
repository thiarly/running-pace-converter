// Botão do menu mobile
const btNav = document.querySelector('#btNav');
const divNav = document.querySelector('#divNav');

// Toggle do menu mobile
btNav?.addEventListener('click', () => {
    divNav?.classList.toggle('hidden');
});

// Lista dos dropdowns
const dropdownLinks = [
    { buttonId: '#dropdownNavbarLink1', menuId: '#dropdownNavbar1' },
    { buttonId: '#dropdownNavbarLink2', menuId: '#dropdownNavbar2' },
    { buttonId: '#dropdownNavbarLink3', menuId: '#dropdownNavbar3' },
    { buttonId: '#dropdownNavbarLink4', menuId: '#dropdownNavbar4' }
];

// Fecha todos os dropdowns
function closeAllDropdowns(exceptId = null) {
    dropdownLinks.forEach(link => {
        if (link.menuId !== exceptId) {
            const el = document.querySelector(link.menuId);
            el?.classList.add('hidden');
        }
    });
}

// Alterna dropdown (fechando os demais)
function toggleDropdown(dropdownId) {
    const menu = document.querySelector(dropdownId);
    const isHidden = menu?.classList.contains('hidden');
    closeAllDropdowns(dropdownId);
    if (isHidden) {
        menu?.classList.remove('hidden');
    } else {
        menu?.classList.add('hidden');
    }
}

// Adiciona listeners aos botões
dropdownLinks.forEach(link => {
    const button = document.querySelector(link.buttonId);
    button?.addEventListener('click', e => {
        e.stopPropagation();
        toggleDropdown(link.menuId);
    });
});

document.getElementById('userDropdown')?.addEventListener('click', () => {
    const menu = document.getElementById('dropdownUserMenu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
});


// Fecha dropdowns ao clicar fora
document.addEventListener('click', () => closeAllDropdowns());




// static/js/flash.js
setTimeout(() => {
    document.querySelectorAll('.flash-message').forEach(el => {
      // @ts-ignore
      el.style.transition = "opacity 0.5s ease";
      // @ts-ignore
      el.style.opacity = 0;
      setTimeout(() => el.remove(), 500);
    });
  }, 2000);
  


  function toggleResumo(id) {
    const el = document.getElementById(id);
    // @ts-ignore
    el.classList.toggle("hidden");
  }
