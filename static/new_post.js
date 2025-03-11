const select = document.getElementById("type");

function select_type() {
    if (select.value == "all") {
        following.setAttribute("hidden", "hidden")
        all.removeAttribute("hidden");
    } else {
        all.setAttribute("hidden", "hidden");
        following.removeAttribute("hidden");
    }
}