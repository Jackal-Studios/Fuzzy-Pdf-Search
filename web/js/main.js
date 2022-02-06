alert('123');
// const electron = require('electron')
// Importing BrowserWindow from Main Process
// const BrowserWindow = electron.remote.BrowserWindow;
  
// var find = document.getElementById('find');
// var clear = document.getElementById('clear');
// let win = BrowserWindow.getFocusedWindow();
// // let win = BrowserWindow.getAllWindows()[0];
  
// var options = {
//     forward: true,
//     findNext: false,
//     matchCase: false,
//     wordStart: false,
//     medialCapitalAsWordStart: false
// }
  
// find.addEventListener('click', () => {
//     var text = document.getElementById('enter').value;
//     console.log(text);
//     if (text) {
//         const requestId = win.webContents.findInPage(text, options);
//         console.log(requestId);
//     } else {
//         console.log('Enter Text to find');
//     }
  
//     win.webContents.on('found-in-page', (event, result) => {
//         console.log(result.requestId);
//         console.log(result.activeMatchOrdinal);
//         console.log(result.matches);
//         console.log(result.selectionArea);
//     });
// });
  
// clear.addEventListener('click', () => {
//     win.webContents.stopFindInPage('clearSelection');
// });



document.getElementById("button-name").addEventListener("click", ()=>{eel.get_random_name()}, false);
document.getElementById("button-number").addEventListener("click", ()=>{eel.get_random_number()}, false);
document.getElementById("button-date").addEventListener("click", ()=>{eel.get_date()}, false);
document.getElementById("button-ip").addEventListener("click", ()=>{eel.get_ip()}, false);

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}