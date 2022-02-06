// Modules to control application life and create native browser window
const {app, BrowserWindow, globalShortcut, ipcMain} = require('electron')
const url = require("url")
const path = require("path")
const electronmine = require('electron')
//const BrowserWindow = electronmine.remote.BrowserWindow;

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    icon: 'web/index_files/icon.ico',
    webPreferences: {
      nodeIntegrationInSubFrames: true,
      nodeIntegration: true,
      webviewTag: true,
      webSecurity: false,
      enableRemoteModule: true,
      preload: path.join(__dirname, "preload.js")
    }
    
  })
  mainWindow.maximize();
  mainWindow.setMenu(null);
  // and load the index.html of the app.
  mainWindow.loadURL('http://localhost:8000/index.html');
  

  mainWindow.toggleDevTools()
  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('focus', () => {
    globalShortcut.register('CommandOrControl+F', function () {

      if (mainWindow && mainWindow.webContents) {
         mainWindow.webContents.send('on-find', '')

      }
    })
  })
  mainWindow.on('blur', () => {
    globalShortcut.unregister('CommandOrControl+F')
  })
  


  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

ipcMain.on("toMain", (event, args) => {
    // Do something with file contents

    // Send result back to renderer process
    text=args;

    mainWindow.webContents.send("fromMain", args);
    //mainWindow.webContents.send("fromMain", args+"1");

    let win = BrowserWindow.getFocusedWindow();
    if(text=="stop1"){
          win.webContents.stopFindInPage('clearSelection');
          mainWindow.webContents.send("fromMain", "true");

    }
    //mainWindow.webContents.send("fromMain", "false");

    var options = {
    forward: true,
    findNext: false,
    matchCase: false,
    wordStart: false,
    medialCapitalAsWordStart: false
    }
    const requestId = mainWindow.webContents.findInPage(text, options);
        mainWindow.webContents.send("fromMain", requestId);

        mainWindow.webContents.on('found-in-page', (event, result) => {
        mainWindow.webContents.send("fromMain", "32423434");
        mainWindow.webContents.send("fromMain", result.activeMatchOrdinal);
        mainWindow.webContents.send("fromMain", result.matches);
        mainWindow.webContents.send("fromMain", result.selectionArea);

        console.log(result.requestId);
        console.log(result.activeMatchOrdinal);
        console.log(result.matches);
        console.log(result.selectionArea);
    });
  
});

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.