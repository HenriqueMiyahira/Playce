(function () {
    const menus = document.querySelectorAll('[data-profile-menu]');

    function closeMenu(menu) {
        const trigger = menu.querySelector('[data-profile-trigger]');
        menu.classList.remove('open');

        if (trigger) {
            trigger.setAttribute('aria-expanded', 'false');
        }
    }

    menus.forEach((menu) => {
        const trigger = menu.querySelector('[data-profile-trigger]');

        if (!trigger) {
            return;
        }

        trigger.addEventListener('click', (event) => {
            event.stopPropagation();
            const isOpen = menu.classList.toggle('open');
            trigger.setAttribute('aria-expanded', String(isOpen));
        });
    });

    document.addEventListener('click', (event) => {
        menus.forEach((menu) => {
            if (!menu.contains(event.target)) {
                closeMenu(menu);
            }
        });
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            menus.forEach(closeMenu);
        }
    });

    document.querySelectorAll('[data-logout-form]').forEach((form) => {
        form.addEventListener('submit', () => {
            window.playceAuthState = {
                isLoggedIn: false,
                userName: '',
            };
            window.isLoggedIn = false;
            window.userName = '';
        });
    });
})();
