document.addEventListener("DOMContentLoaded", function () {
    const sidebarLinks = document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function () {
            const currentCollapse = this.getAttribute('href') || this.dataset.bsTarget;

            sidebarLinks.forEach(otherLink => {
                const otherCollapse = otherLink.getAttribute('href') || otherLink.dataset.bsTarget;

                if (otherCollapse !== currentCollapse) {
                    const collapseElement = document.querySelector(otherCollapse);
                    if (collapseElement && collapseElement.classList.contains('show')) {
                        new bootstrap.Collapse(collapseElement, { toggle: true });
                    }
                }
            });
        });
    });
});
