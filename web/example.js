alert('1');
//const { remote, ipcRenderer } = require('electron')
//const { FindInPage } = require('../node_modules/electron-find/src/index.js')
//import { remote , ipcRenderer } from "E:/PythonProjects/Fuzzy-Pdf-Search/node_modules/@electron/get/dist/cjs/index.js";
const { remote, ipcRenderer } = require('electron');
//import {ipcRenderer} from "electron";
//import { FindInPage} from "E:/PythonProjects/Fuzzy-Pdf-Search/node_modules/electron-find/src/index.js";
import "E:/PythonProjects/Fuzzy-Pdf-Search/node_modules/electron-find/src/findInPage.js";
let findInPage = new FindInPage(remote.getCurrentWebContents(), {
  preload: true,
  offsetTop: 6,
  offsetRight: 10
})

// let findInPage = new FindInPage(remote.getCurrentWebContents(), {
//   boxBgColor: '#333',
//   boxShadowColor: '#000',
//   inputColor: '#aaa',
//   inputBgColor: '#222',
//   inputFocusColor: '#555',
//   textColor: '#aaa',
//   textHoverBgColor: '#555',
//   caseSelectedColor: '#555',
//   offsetTop: 8,
//   offsetRight: 12
// })

ipcRenderer.on('on-find', (e, args) => {
  alert('123');
  findInPage.openFindWindow()
})

function onChange () {
  alert("77");
  const titleDom = document.querySelector('#title')
  titleDom.innerHTML = '123'
  setTimeout(() => {
    findInPage.update()
  }, 20)
}