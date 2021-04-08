const canvas = document.querySelector(".canvas");

canvas.addEventListener("click", drawNode);

let drawingMode = true;

function drawNode(e) {
  if (drawingMode) {
    const node = document.createElement("div");
    const nodeNameInput = document.createElement("input");
    nodeNameInput.classList.add("node-name-input");
    nodeNameInput.setAttribute("autofocus", true);
    nodeNameInput.setAttribute("placeholder", "Input letter and press enter");
    node.classList.add("node");
    nodeNameInput.addEventListener("keyup", (e) => {
      if (e.code === "Enter") {
        submitNode(e, node);
      }
    });
    node.addEventListener("click", nodeClick);
    node.addEventListener("mouseenter", () => {
      drawingMode = false;
    });
    node.addEventListener("mouseleave", () => {
      drawingMode = true;
    });
    const cursorPos = getCursorPosition(e);
    node.style.left = cursorPos.x + "px";
    node.style.top = cursorPos.y + "px";

    e.target.append(node);
    node.append(nodeNameInput);
    console.log(e);
  }
}

function nodeClick(e) {
  console.log(e);
}

function getCursorPosition(e) {
  var mouseX = e.offsetX;
  var mouseY = e.offsetY;
  return { x: mouseX, y: mouseY };
}

const variables = [];

function submitNode(e, node) {
  const val = e.target.value;
  if (variables.includes(val)) {
    alert("Variable already exists!\nInput another variable");
    return;
  }
  node.setAttribute("id", val);
  node.append(val);
  e.target.style.display = "none";
  variables.push(val);
}
