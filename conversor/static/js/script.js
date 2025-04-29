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

// Fecha dropdowns ao clicar fora
document.addEventListener('click', () => closeAllDropdowns());