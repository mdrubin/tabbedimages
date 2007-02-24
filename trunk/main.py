# Tabbed Image Viewer
# (c) 2007 Andrzej Krzywda, Christian Muirhead & Michael Foord
# email: fuzzyman AT voidspace DOT org DOT uk
# web:   http://www.voidspace.org.uk/ironpython/
#

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import sys
from about import AboutDialog
from icons import (
    CloseIcon, CopyIcon,
    OpenIcon, PasteIcon,
    SaveIcon, ViewIcon
)

from cPickle import loads
from System import ArgumentException
from System.Drawing import Bitmap, Color, Icon
from System.Drawing.Imaging import ImageFormat
from System.IO import Path
from System.Windows.Forms import (
    Application, Clipboard, ControlStyles, ContextMenuStrip,
    DataObject, DialogResult, DockStyle, DragDropEffects,
    Form, ImageList, Keys, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, Panel, PictureBox, PictureBoxSizeMode,
    SaveFileDialog, TabControl, TabAlignment,
    TabPage, ToolStrip, ToolStripButton,
    ToolStripMenuItem, ToolStripItemDisplayStyle
)


try:
    clr.AddReference('Clipboard.dll')
except IOError:
    SetClipboardViewer = None
else:
    from Clipboard import Clipboard as SetClipboardViewer


FILTER = ("Images (*.JPG;*.BMP;*.GIF;*.PNG;*.TIF;*.ICO)|"
          "*.JPG;*.BMP;*.GIF;*.PNG;*.TIF;*.ICO|"
          "All files (*.*)|*.*")
IMAGEPATH = Path.GetFullPath(Path.Combine(Path.GetDirectoryName(sys.argv[0]), "images"))
IMAGEFORMATS = {'.jpg': ImageFormat.Jpeg,
                '.jpeg': ImageFormat.Jpeg,
                '.bmp': ImageFormat.Bmp,
                '.gif': ImageFormat.Gif,
                '.png': ImageFormat.Png,
                '.tif': ImageFormat.Tiff,
                '.ico': ImageFormat.Icon
                }
CLIPBOARD_DRAW = 0x0308
WM_CHANGECBCHAIN = 0x030D


class ScrollableImagePanel(Panel):

    def __init__(self, pictureBox):
        Panel.__init__(self)

        # This makes the panel selectable, and therefore scrollable
        # with the mouse wheel
        self.SetStyle(ControlStyles.Selectable, True)
        self.Dock = DockStyle.Fill
        self.AutoScroll = True

        self.image = pictureBox.Image
        self.sizeMode = pictureBox.SizeMode

        pictureBox.Parent = self
        pictureBox.Click += lambda *_: self.Focus()
        self.Click += lambda *_: self.Focus()


    def IsInputKey(self, key):
        if key in (Keys.Left, Keys.Right):
            return True
        return False


class DialogManager(object):
        
    def getOpenFileDialog(self, **kwargs):
        return OpenFileDialog(**kwargs)
        

class MainForm(Form):

    def __init__(self, openFileDialog=None):
        Form.__init__(self)
        if openFileDialog:
            self.openFileDialog = openFileDialog
        else:
            self.openFileDialog = OpenFileDialog()
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        self.Icon = Icon(Path.Combine(IMAGEPATH, "pictures.ico"))
        self.AllowDrop = True
        self.justCopied = False
        self.paths = []
        
        self.initTabControl()
        self.initToolBar()
        self.initMenu()
        self.initContextMenu()
        
        self._clipboardViewerNext = None
        if SetClipboardViewer is not None:
            self._clipboardViewerNext = SetClipboardViewer.SetClipboardViewer(self.Handle)

        for fileName in sys.argv[1:]:
            self.openFile(fileName)

        self.updateToolbar()
        
        self.DragEnter += self.onDragEnter


    def WndProc(self, msg):
        if self._clipboardViewerNext is None:
            return Form.WndProc(self, msg)
        message = msg.Value
        if message.Msg == CLIPBOARD_DRAW:
            self.onPaste(None, None)
            SetClipboardViewer.SendMessage(self._clipboardViewerNext, 
                                           message.Msg, 
                                           message.WParam,
                                           message.LParam)
        elif message.Msg == WM_CHANGECBCHAIN:
            if message.WParam == self._clipboardViewerNext:
                self._clipboardViewerNext = message.LParam
            else:
                SetClipboardViewer.SendMessage(self._clipboardViewerNext, 
                                               message.Msg, 
                                               message.WParam,
                                               message.LParam)
        else:
            Form.WndProc(self, msg)

    
    def Dispose(self, disposing):
        if SetClipboardViewer is not None:
            SetClipboardViewer.ChangeClipboardChain(self.Handle, self._clipboardViewerNext)
        Form.Dispose(self, disposing)
       
       
    def onDragEnter(self, source, event):
        if event.Data.ContainsFileDropList():
            event.Effect = DragDropEffects.Copy
        else:
            event.Effect = DragDropEffects.None
    
    def initTabControl(self):
        self.tabControl = TabControl(
            Name = "TabControl",
            Dock = DockStyle.Fill,
            Alignment = TabAlignment.Bottom
        )
        self.Controls.Add(self.tabControl)
        self.tabControl.SelectedIndexChanged += self.onSelectedIndexChanged


    def createMenuItem(self, name, text, clickHandler=None, keys=None):
        menuItem = ToolStripMenuItem(
            Name = name,
            Text = text
        )
        if keys:
            menuItem.ShortcutKeys = keys
        if clickHandler:
            menuItem.Click += clickHandler
        return menuItem


    def initMenu(self):
        menuStrip = MenuStrip(
            Name = "Main MenuStrip",
            Dock = DockStyle.Top
        )
        fileMenu      = self.createMenuItem('File Menu', '&File')
        openMenuItem  = self.createMenuItem('Open', '&Open...', self.onOpen,
                                            keys=(Keys.Control | Keys.O))
        saveMenuItem  = self.createMenuItem('Save', '&Save...', self.onSave,
                                            keys=(Keys.Control | Keys.S))
        closeMenuItem = self.createMenuItem('Close', '&Close', self.onClose,
                                            keys=(Keys.Control | Keys.W))
        exitMenuItem  = self.createMenuItem('Exit', 'E&xit', lambda *_: Application.Exit(),
                                            keys=(Keys.Control | Keys.X))

        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(saveMenuItem)
        fileMenu.DropDownItems.Add(closeMenuItem)
        fileMenu.DropDownItems.Add(exitMenuItem)

        editMenu = self.createMenuItem('Edit Menu', '&Edit')
        copy =  self.createMenuItem('Copy', '&Copy', self.onCopy,
                                    keys=(Keys.Control | Keys.C))
        paste = self.createMenuItem('Paste', '&Paste', self.onPaste,
                                    keys=(Keys.Control | Keys.V))
        view = self.createMenuItem('Image Mode', '&Image Mode', self.onImageMode,
                                   keys=(Keys.Control | Keys.I))
        editMenu.DropDownItems.Add(copy)
        editMenu.DropDownItems.Add(paste)
        editMenu.DropDownItems.Add(view)

        helpMenu = self.createMenuItem('Help Menu', '&Help')
        about =  self.createMenuItem('About', '&About...', self.onAbout)
        helpMenu.DropDownItems.Add(about)

        menuStrip.Items.Add(fileMenu)
        menuStrip.Items.Add(editMenu)
        menuStrip.Items.Add(helpMenu)
        self.Controls.Add(menuStrip)


    def initContextMenu(self):
        contextMenuStrip = ContextMenuStrip()
        contextMenuStrip.Items.Add(self.createMenuItem('Copy', '&Copy', self.onCopy))
        contextMenuStrip.Items.Add(self.createMenuItem('Paste', '&Paste', self.onPaste))
        contextMenuStrip.Items.Add(self.createMenuItem('Close', '&Close', self.onClose))
        contextMenuStrip.Items.Add(self.createMenuItem('Image Mode', '&Image Mode', self.onImageMode))
        self.tabControl.ContextMenuStrip = contextMenuStrip


    def initToolBar(self):
        self.activeWithImages = []
        
        self.toolBar = ToolStrip(
            Dock = DockStyle.Top
        )

        def addToolBarIcon(pickledIcon, name, clickHandler, checkOnClick=False):
            button = ToolStripButton()
            if pickledIcon:
                button.Image = loads(pickledIcon)
            button.ImageTransparentColor = Color.Magenta
            button.ToolTipText = button.Name = name
            button.DisplayStyle = ToolStripItemDisplayStyle.Image
            if clickHandler:
                button.Click += clickHandler
            if checkOnClick:
                button.CheckOnClick = True
            self.toolBar.Items.Add(button)
            return button

        addToolBarIcon(OpenIcon, "Open", self.onOpen)
        save = addToolBarIcon(SaveIcon, "Save", self.onSave)
        self.activeWithImages.append(save)
        
        close = addToolBarIcon(CloseIcon, "Close", self.onClose)
        self.activeWithImages.append(close)
        
        copy = addToolBarIcon(CopyIcon, "Copy", self.onCopy)
        self.activeWithImages.append(copy)
        
        addToolBarIcon(PasteIcon, "Paste", self.onPaste)
        mode = addToolBarIcon(ViewIcon, "Image mode", self.onImageMode, True)
        self.activeWithImages.append(mode)
        self.imageModeButton = mode

        self.Controls.Add(self.toolBar)


    def onKeyDown(self, _, event):
        if (self.tabControl.SelectedTab is None or
            len(self.tabControl.TabPages) == 1):
            return
        if event.KeyCode == Keys.Right:
            modifier = 1
        elif event.KeyCode == Keys.Left:
            modifier = -1
        else:
            return

        selected = self.tabControl.SelectedIndex
        selected += modifier
        if selected == len(self.paths):
            self.tabControl.SelectedIndex = 0
        elif selected < 0:
            self.tabControl.SelectedIndex = len(self.paths) - 1
        else:
            self.tabControl.SelectedIndex = selected

        self.tabControl.SelectedTab.Controls[0].Focus()


    def onSelectedIndexChanged(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab is not None:
            self.imageModeButton.Checked = selectedTab.Controls[0].sizeMode == PictureBoxSizeMode.StretchImage


    def getImage(self, fileName):
        try:
            return Bitmap(fileName)
        except ArgumentException:
            MessageBox.Show(fileName + " doesn't appear to be a valid image file",
                            "Invalid image format",
                            MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
            return None


    def getPictureBox(self, image, mode=PictureBoxSizeMode.AutoSize):
        keyWArgs = {'Image': image,
                    'SizeMode': mode}
        if mode == PictureBoxSizeMode.StretchImage:
            keyWArgs['Dock'] = DockStyle.Fill
        return PictureBox(**keyWArgs)


    def createTab(self, image, filePath=None):
        if filePath is not None:
            name = Path.GetFileName(filePath)
            directory = Path.GetDirectoryName(filePath)
        else:
            name = "CLIPBOARD"
            directory = None

        tabPage = TabPage()
        tabPage.Text = name
        panel = ScrollableImagePanel(self.getPictureBox(image))
        panel.KeyDown += self.onKeyDown
        tabPage.Controls.Add(panel)

        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage

        self.paths.insert(self.tabControl.SelectedIndex, (name, directory))


    def onOpen(self, _, __):
        self.openFileDialog.Filter = FILTER
        self.openFileDialog.Multiselect = True

        if self.openFileDialog.ShowDialog() == DialogResult.OK:
            for fileName in self.openFileDialog.FileNames:
                self.openFile(fileName)
        self.updateToolbar()


    def openFile(self, fileName):
        image = self.getImage(fileName)
        if image:
            self.createTab(image, fileName)


    def onClose(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            self.tabControl.TabPages.Remove(selectedTab)
            del self.paths[self.tabControl.SelectedIndex]
        self.updateToolbar()


    def onCopy(self, _, __):
        self.justCopied = True
        dataObject = DataObject()
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            dataObject.SetImage(selectedTab.Controls[0].image)
            Clipboard.SetDataObject(dataObject)


    def onPaste(self, _, __):
        if self.justCopied:
            self.justCopied = False
            return
        dataObject = Clipboard.GetDataObject()
        if dataObject.ContainsImage():
            self.createTab(dataObject.GetImage())
            self.updateToolbar()


    def onSave(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            (name, directory) = self.paths[self.tabControl.SelectedIndex]
            image = selectedTab.Controls[0].image
            saveFileDialog = SaveFileDialog()
            saveFileDialog.Filter = FILTER
            if directory is not None:
                saveFileDialog.InitialDirectory = directory
                saveFileDialog.FileName = name

            if saveFileDialog.ShowDialog() == DialogResult.OK:
                fileName = saveFileDialog.FileName
                extension = Path.GetExtension(fileName)
                format = IMAGEFORMATS.get(extension.lower())
                if format is None:
                    format = ImageFormat.Jpeg
                    fileName += '.jpg'

                try:
                    image.Save(fileName, format)
                except Exception, e:
                    MessageBox.Show("Problem Saving %s.\r\nError: %s" % (fileName, str(e)),
                                    "Problem Saving File",
                                    MessageBoxButtons.OK, MessageBoxIcon.Error)
                
                name = Path.GetFileName(fileName)
                selectedTab.Text = name
                self.paths[self.tabControl.SelectedIndex] = (name, Path.GetDirectoryName(fileName))


    def onAbout(self, _, __):
        AboutDialog(IMAGEPATH).ShowDialog()


    def onImageMode(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab is not None:
            currentMode = selectedTab.Controls[0].sizeMode
            image = selectedTab.Controls[0].image
            selectedTab.Controls.RemoveAt(0)
            if currentMode == PictureBoxSizeMode.AutoSize:
                mode = PictureBoxSizeMode.StretchImage
            else:
                mode = PictureBoxSizeMode.AutoSize

            panel = ScrollableImagePanel(self.getPictureBox(image, mode))
            panel.KeyDown += self.onKeyDown
            selectedTab.Controls.Add(panel)


    def updateToolbar(self):
        enableState = False
        if len(self.tabControl.TabPages):
            enableState = True
        for item in self.activeWithImages:
            item.Enabled = enableState


Application.EnableVisualStyles()
if __name__ == "__main__":
    Application.Run(MainForm())
