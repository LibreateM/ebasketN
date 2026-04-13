
function toggleCode() {
    let box = document.getElementById("codeBox");
    box.style.display = box.style.display === "none" ? "block" : "none";
}

function copyCode() {
    let text = document.getElementById("codeBox").innerText;
    navigator.clipboard.writeText(text);
    alert("Code Copied!");
}
