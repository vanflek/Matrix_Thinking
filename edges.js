"use strict";

const size = 8;

function differences(image) {
  const dx = image.map((row) => row.map((value, col) =>
    col ? Math.abs(value - row[col - 1]) : 0));
  const dy = image.map((row, r) => row.map((value, col) =>
    r ? Math.abs(value - image[r - 1][col]) : 0));
  const edges = dx.map((row, r) => row.map((value, col) =>
    Math.max(value, dy[r][col])));
  return { x: dx, y: dy, edges };
}

function pattern(name) {
  return Array.from({ length: size }, (_, row) =>
    Array.from({ length: size }, (_, col) => {
      if (name === "square") return Number(row >= 2 && row <= 5 && col >= 2 && col <= 5);
      if (name === "stairs") return Number(row >= 2 && row <= 6 && col >= 1 && col <= row);
      if (name === "stripes") return Number(col % 3 === 1);
      return 0;
    }));
}

const byId = (id) => document.getElementById(id);
const preset = byId("edge-pattern");
const axis = byId("edge-axis");
const numbers = byId("edge-numbers");
let image = pattern(preset.value);
let selected = 18;

function makeGrid(id, editable) {
  const grid = byId(id);
  return Array.from({ length: size * size }, (_, index) => {
    const cell = document.createElement(editable ? "button" : "span");
    cell.className = "edge-cell";
    if (editable) {
      cell.type = "button";
      cell.addEventListener("click", () => {
        const row = Math.floor(index / size);
        const col = index % size;
        image[row][col] = 1 - image[row][col];
        selected = index;
        render();
      });
      cell.addEventListener("focus", () => {
        selected = index;
        render();
      });
    }
    grid.append(cell);
    return cell;
  });
}

const input = makeGrid("edge-input", true);
const diff = makeGrid("edge-diff", false);
const output = makeGrid("edge-output", false);

function paint(cells, matrix, editable = false) {
  cells.forEach((cell, index) => {
    const row = Math.floor(index / size);
    const col = index % size;
    const value = matrix[row][col];
    cell.textContent = numbers.checked ? value : "";
    cell.classList.toggle("on", value === 1);
    cell.classList.toggle("selected", index === selected);
    if (editable) {
      cell.setAttribute("aria-label", `Row ${row}, column ${col}`);
      cell.setAttribute("aria-pressed", String(value === 1));
    }
  });
}

function render() {
  const result = differences(image);
  const horizontal = axis.value === "x";
  const row = Math.floor(selected / size);
  const col = selected % size;
  const hasNeighbour = horizontal ? col > 0 : row > 0;
  const comparison = hasNeighbour
    ? `|${image[row][col]} − ${horizontal ? image[row][col - 1] : image[row - 1][col]}| = ${result[axis.value][row][col]}`
    : "No neighbour in this direction, so the difference is 0";
  paint(input, image, true);
  paint(diff, result[axis.value]);
  paint(output, result.edges);
  byId("edge-caption").textContent = horizontal
    ? "Subtract the left neighbour to reveal vertical edges."
    : "Subtract the upper neighbour to reveal horizontal edges.";
  byId("edge-inspect").textContent =
    `image[${row}, ${col}]. ${comparison}. Combined edge value: ${result.edges[row][col]}.`;
}

function reset() {
  image = pattern(preset.value);
  selected = 18;
  render();
}

preset.addEventListener("change", reset);
byId("edge-reset").addEventListener("click", reset);
axis.addEventListener("change", render);
numbers.addEventListener("change", render);
render();
