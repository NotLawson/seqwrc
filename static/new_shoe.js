function add_tag() {
    const tag = document.getElementById("tag");
    const tag_div = document.getElementById("tags");
    var clone = tag.cloneNode(true);
    clone.value="";
    tag_div.appendChild(clone);
    tag_div.appendChild(document.createElement("br"));
}