const btNav = document.querySelector('#btNav');
const divNav = document.querySelector('#divNav');

// @ts-ignore
btNav.addEventListener('click', function() {
    // @ts-ignore
    divNav.classList.toggle('hidden');
})

