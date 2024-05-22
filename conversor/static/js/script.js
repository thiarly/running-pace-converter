// @ts-nocheck
const btNav = document.querySelector('#btNav');
const divNav = document.querySelector('#divNav');

// Alternar visibilidade do menu principal em dispositivos móveis
btNav.addEventListener('click', function() {
    divNav.classList.toggle('hidden');
});

// Função para alternar a visibilidade do dropdown
function toggleDropdown(dropdownId) {
    const dropdownMenu = document.querySelector(dropdownId);
    dropdownMenu.classList.toggle('hidden');
}

// Função para fechar dropdowns se clicar fora
function closeDropdowns(event) {
    dropdownLinks.forEach(link => {
        const dropdownMenu = document.querySelector(link.menuId);
        if (!dropdownMenu.contains(event.target) && !document.querySelector(link.buttonId).contains(event.target) && !dropdownMenu.classList.contains('hidden')) {
            // @ts-ignore
            dropdownMenu.classList.add('hidden');
        }
    });
}

// Event listeners para botões de dropdown
const dropdownLinks = [
    { buttonId: '#dropdownNavbarLink1', menuId: '#dropdownNavbar1' },
    { buttonId: '#dropdownNavbarLink2', menuId: '#dropdownNavbar2' },
    { buttonId: '#dropdownNavbarLink3', menuId: '#dropdownNavbar3' }
];

dropdownLinks.forEach(link => {
    const button = document.querySelector(link.buttonId);
    button.addEventListener('click', () => toggleDropdown(link.menuId));
});

// Adiciona o listener ao documento para fechar os dropdowns ao clicar fora
document.addEventListener('click', closeDropdowns);
