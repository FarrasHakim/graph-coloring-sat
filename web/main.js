const canvasDiv = document.querySelector(".canvas");
const canvas = document.querySelector("#canvas");
let ctx = canvas.getContext("2d");

canvasDiv.addEventListener("click", drawNode);

let canAddNode = true;
let stillInputNode = false;

function drawNode(e) {
  if (canAddNode && !stillInputNode) {
    stillInputNode = true;
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
      canAddNode = false;
    });
    node.addEventListener("mouseleave", () => {
      canAddNode = true;
    });
    const cursorPos = getCursorPosition(e);
    node.style.left = cursorPos.x + "px";
    node.style.top = cursorPos.y + "px";

    e.target.append(node);
    node.append(nodeNameInput);
  }
}
let constraint = {
  current: null,
  other: null,
};
let constraints = [];
function nodeClick(e) {
  if (stillInputNode) {
    return;
  }
  console.log("test");
  const id = e.target.getAttribute("id");
  if (!constraint.current) constraint.current = id;
  else if (!constraint.other) {
    constraint.other = id;
    const tempConstraint = constraint.current + "!=" + constraint.other;
    if (constraints.includes(tempConstraint)) return;
    constraints.push(tempConstraint);
    const currentNode = document.getElementById(constraint.current);
    const otherNode = document.getElementById(constraint.other);
    const curX = parseInt(currentNode.style.left.split("px")[0]);
    const curY = parseInt(currentNode.style.top.split("px")[0]);
    const othX = parseInt(otherNode.style.left.split("px")[0]);
    const othY = parseInt(otherNode.style.top.split("px")[0]);
    console.log();
    linedraw(curX, curY, othX, othY);
    constraint = {
      current: null,
      other: null,
    };
  }
}

function getCursorPosition(e) {
  var mouseX = e.offsetX;
  var mouseY = e.offsetY;
  return { x: mouseX, y: mouseY };
}

function linedraw(ax, ay, bx, by) {
  const distance = Math.sqrt((ax - bx) * (ax - bx) + (ay - by) * (ay - by));
  xMid = (ax + bx) / 2;
  yMid = (ay + by) / 2;

  salopeInRadian = Math.atan2(ay - by, ax - bx);
  salopeInDegrees = (salopeInRadian * 180) / Math.PI;

  const line = document.createElement("div");
  line.classList.add("line");
  line.style.width = distance;
  line.style.width = distance + "px";
  line.style.top = yMid + "px";
  line.style.left = xMid - distance / 2 + "px";
  line.style.transform = "rotate(" + salopeInDegrees + "deg)";
  canvasDiv.append(line);
}

function drawLine(ctx, begin, end, stroke = "black", width = 1) {
  if (stroke) {
    ctx.strokeStyle = stroke;
  }

  if (width) {
    ctx.lineWidth = width;
  }
  ctx.beginPath();
  ctx.moveTo(...begin);
  ctx.lineTo(...end);
  ctx.stroke();
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
  stillInputNode = false;
}
