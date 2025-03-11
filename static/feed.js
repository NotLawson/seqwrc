const following = document.getElementById("following");
const all = document.getElementById("all");

const following_button = document.getElementById("following_button");
const all_button = document.getElementById("all_button");


function select_all() {
    console.log("select_all");
    following_button.classList.remove("selected")
    all_button.classList.add("selected")
    following.setAttribute("hidden", "hidden")
    all.removeAttribute("hidden");
}

function select_following() {
    console.log("select_following");
    all_button.classList.remove("selected")
    following_button.classList.add("selected")
    all.setAttribute("hidden", "hidden");
    following.removeAttribute("hidden");
}