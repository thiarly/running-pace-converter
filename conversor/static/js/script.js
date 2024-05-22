const btNav = document.querySelector('#btNav');
const divNav = document.querySelector('#divNav');

// Alternar visibilidade do menu principal em dispositivos móveis
// @ts-ignore
btNav.addEventListener('click', function() {
    // @ts-ignore
    divNav.classList.toggle('hidden');
});

// Função para alternar a visibilidade do dropdown
function toggleDropdown(dropdownId) {
    const dropdownMenu = document.querySelector(dropdownId);
    dropdownMenu.classList.toggle('hidden');
}

// Event listeners para botões de dropdown
const dropdownLinks = [
    { buttonId: '#dropdownNavbarLink', menuId: '#dropdownNavbar' },
    { buttonId: '#dropdownNavbarLink2', menuId: '#dropdownNavbar2' },
    { buttonId: '#dropdownNavbarLink3', menuId: '#dropdownNavbar3' }
];

dropdownLinks.forEach(link => {
    const button = document.querySelector(link.buttonId);
    // @ts-ignore
    button.addEventListener('click', () => toggleDropdown(link.menuId));
});