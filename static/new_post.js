const select = document.getElementById("type");

const post = document.getElementById("post");
const run = document.getElementById("run");
const ev = document.getElementById("event");

function select_type() {
    if (select.value == "post") {
        ev.setAttribute("hidden", "hidden");
        run.setAttribute("hidden", "hidden")
        post.removeAttribute("hidden");
    } else if (select.value == "run") {
        ev.setAttribute("hidden", "hidden");
        post.setAttribute("hidden", "hidden")
        run.removeAttribute("hidden");
    } else {
        post.setAttribute("hidden", "hidden")
        run.setAttribute("hidden", "hidden")
        ev.removeAttribute("hidden");
    }
}