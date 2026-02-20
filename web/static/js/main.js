document.addEventListener("DOMContentLoaded", function () {
    const dateEl = document.getElementById("current-date");
    if (dateEl) {
        const now = new Date();
        dateEl.textContent = now.toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        });
    }

    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {
        if (item.href === window.location.href) {
            item.classList.add("active");
        }
    });
});