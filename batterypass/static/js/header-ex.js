function toggleContent(elementId, arrowId) {
    var content = document.getElementById(elementId);
    var arrow = document.getElementById(arrowId);

    if (content.classList.contains("hidden")) {
        arrow.textContent = "▲";
        content.classList.remove("hidden");
    } else {
        arrow.textContent = "▼";
        content.classList.add("hidden");
    }
}

