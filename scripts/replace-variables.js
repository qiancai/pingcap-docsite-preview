#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function getValueByPath(obj, pathStr) {
  return pathStr.split(".").reduce((acc, key) => (acc ? acc[key] : ""), obj) ?? "";
}

const variablePattern = /{{{\s*\.(.+?)\s*}}}/g;

function replaceVariablesInFile(filePath, variables) {
  let content = fs.readFileSync(filePath, "utf-8");
  content = content.replace(variablePattern, (_, path) => {
    const value = getValueByPath(variables, path.trim());
    if (value) {
      return String(value);
      }
    return match;
  });
  fs.writeFileSync(filePath, content, "utf-8");
}

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach((f) => {
    const dirPath = path.join(dir, f);
    const isDirectory = fs.statSync(dirPath).isDirectory();
    if (isDirectory) {
      walkDir(dirPath, callback);
    } else {
      callback(path.join(dir, f));
    }
  });
}

const dir = process.argv[2]; // Target directory
const variablesPath = process.argv[3]; // Path to variables.json

if (!fs.existsSync(dir) || !fs.existsSync(variablesPath)) {
  console.error("Usage: node replace-variables.js <dir> <variables.json>");
  process.exit(1);
}

const variables = JSON.parse(fs.readFileSync(variablesPath, "utf-8"));

walkDir(dir, (filePath) => {
  if (filePath.endsWith(".md")) {
    replaceVariablesInFile(filePath, variables);
  }
});
