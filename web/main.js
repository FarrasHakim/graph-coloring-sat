const canvasDiv = document.querySelector(".canvas");
const canvas = document.querySelector("#canvas");
const addDomainBtn = document.querySelector(".add-domain");
const domainContainer = document.querySelector(".add-domain__container");
const colorTheGraphButton = document.getElementById("color-graph");
let ctx = canvas.getContext("2d");

canvasDiv.addEventListener("click", drawNode);
addDomainBtn.addEventListener("click", addDomain);
colorTheGraphButton.addEventListener("click", colorTheGraph);

function colorTheGraph() {
  const domains = getDomains();
  const variables = variableList;
  const constraints = constraintList;

  eel.color_the_graph(domains, variables, constraints)(setColorGraph);
}

function setColorGraph(data) {
  console.log(data);
  // const modelList = data.split(" ");
  // for (const model of modelList) {
  //   const variable = model.split("_")[0];
  //   const color = model.split("_")[1];
  //   const node = document.getElementById(variable);
  //   node.style.backgrounColor = color;
  // }
}

function addDomain(e) {
  const domainInput = document.createElement("input");
  domainInput.setAttribute("type", "color");
  domainInput.value = "#ffffff";
  domainInput.classList.add("domain");
  const domains = getDomains();
  if (domains.includes(domainInput.value)) {
    alert("Ubah domain warna yang berwarna putih!");
    return;
  }
  domainContainer.append(domainInput);
}

function getDomains() {
  const temp = [];
  document.querySelectorAll(".domain").forEach((e) => {
    temp.push(e.value);
  });
  return temp;
}

let canAddNode = true;
let stillInputNode = false;
let drawingMode = true;
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
let constraintList = [];
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
    if (constraintList.includes(tempConstraint)) return;
    constraintList.push(tempConstraint);
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

const variableList = [];

function submitNode(e, node) {
  const val = e.target.value;
  if (variableList.includes(val)) {
    alert("Variable already exists!\nInput another variable");
    return;
  }
  node.setAttribute("id", val);
  node.append(val);
  e.target.style.display = "none";
  stillInputNode = false;
  variableList.push(val);
}
