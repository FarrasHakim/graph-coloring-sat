const canvasDiv = document.querySelector(".canvas");
const canvas = document.querySelector("#canvas");
const addDomainBtn = document.querySelector(".add-domain");
const domainContainer = document.querySelector(".add-domain__container");
const colorTheGraphButton = document.getElementById("color-graph");

canvasDiv.addEventListener("click", drawNode);
addDomainBtn.addEventListener("click", addDomain);
colorTheGraphButton.addEventListener("click", colorTheGraph);

function allEqual(ls, otherLs) {
  if (!ls || !otherLs) return false;
  for (const data of ls) {
    if (!otherLs.includes(data)) {
      return false;
    }
  }
  return true;
}

function colorTheGraph() {
  let domainSaved = window.localStorage.getItem("domains");
  let variableSaved = window.localStorage.getItem("variables");
  let constraintSaved = window.localStorage.getItem("constraints");

  if (domainSaved && variableSaved && constraintSaved) {
    domainSaved = domainSaved.split(",");
    variableSaved = variableSaved.split(",");
    constraintSaved = constraintSaved.split(",");
  }

  const domains = getDomains();
  const variables = variableList;
  const constraints = constraintList;

  if (variables.length === 0) {
    alert("Make sure you have already input the variables!");
    return;
  } else if (domains.length === 0) {
    alert("Make sure you have already input the domains!");
    return;
  }

  console.log(allEqual(domains, domainSaved));
  console.log(allEqual(variables, variableSaved));
  console.log(allEqual(constraints, constraintSaved));

  if (
    allEqual(domains, domainSaved) &&
    allEqual(variables, variableSaved) &&
    allEqual(constraints, constraintSaved)
  ) {
    eel.recolor_the_graph(variables, domains, constraints)(checkResult);
  } else {
    eel.color_the_graph(variables, domains, constraints)(checkResult);
  }
  window.localStorage.setItem("domains", domains);
  window.localStorage.setItem("variables", variables);
  window.localStorage.setItem("constraints", constraints);
}

function checkResult(data) {
  if (data) setColorGraph(data);
  else alert("UNSATISFIABLE");
}

function setColorGraph(data) {
  const modelList = data.split(" ");
  for (const model of modelList) {
    const variable = model.split("_")[0];
    const color = model.split("_")[1];
    const node = document.getElementById(variable);
    if (node) node.style.backgroundColor = color;
  }
}

function addDomain() {
  const domainInput = document.createElement("input");
  domainInput.setAttribute("type", "color");
  domainInput.value = "#ffffff";
  domainInput.classList.add("domain");
  const domains = getDomains();
  if (domains.includes(domainInput.value)) {
    alert(
      "Domain color already exist! Replace white color with others before you add another color!"
    );
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
