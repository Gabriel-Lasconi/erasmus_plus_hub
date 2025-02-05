document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    // Check user preference from localStorage
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        themeIcon.classList.replace("bi-moon", "bi-sun");
    }

    toggleBtn.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        const isDark = body.classList.contains("dark-mode");

        localStorage.setItem("theme", isDark ? "dark" : "light");
        themeIcon.classList.toggle("bi-moon", !isDark);
        themeIcon.classList.toggle("bi-sun", isDark);
    });
});
