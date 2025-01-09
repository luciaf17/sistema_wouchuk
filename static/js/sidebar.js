document.addEventListener("DOMContentLoaded", function () {
    const mainMenus = document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');

    mainMenus.forEach(mainMenu => {
        mainMenu.addEventListener('click', function () {
            const targetMainMenu = this.dataset.bsTarget;

            // Cerramos otros menús principales
            mainMenus.forEach(otherMainMenu => {
                const otherTargetMainMenu = otherMainMenu.dataset.bsTarget;

                if (otherTargetMainMenu !== targetMainMenu) {
                    const otherCollapse = document.querySelector(otherTargetMainMenu);
                    if (otherCollapse && otherCollapse.classList.contains('show')) {
                        new bootstrap.Collapse(otherCollapse, { toggle: true });
                    }
                }
            });
        });
    });
});
