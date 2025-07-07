document.addEventListener("DOMContentLoaded" , () => {
    const burger = document.querySelector(".burger input");
    const sidebar = document.querySelector(".sidebar");
    const content = document.querySelector(".content")

    burger.addEventListener("change", () => {
        sidebar.classList.toggle("active");
        content.classList.toggle("sidebar-active");
    });
});