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
    DataObject, DialogResult, DockStyle,
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
IMAGEPATH = Path.Combine(Path.GetDirectoryName(sys.argv[0]), "images")
IMAGEFORMATS = {'.jpg': ImageFormat.Jpeg,
                '.jpeg': ImageFormat.Jpeg,
                '.bmp': ImageFormat.Bmp,
                '.gif': ImageFormat.Gif,
                '.png': ImageFormat.Png,
                '.tif': ImageFormat.Tiff,
                '.ico': ImageFormat.Icon
                }
CLIPBOARD_DRAW = 0x0308


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


class MainForm(Form):

    def __init__(self):
        Form.__init__(self)
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        self.Icon = Icon(Path.Combine(IMAGEPATH, "pictures.ico"))

        self.initTabControl()
        self.initToolBar()
        self.initMenu()
        self.initContextMenu()
        
        self.paths = []
        if SetClipboardViewer is not None:
            self._clipboardViewerNext = SetClipboardViewer.SetClipboardViewer(self.Handle)

        for fileName in sys.argv[1:]:
            self.openFile(fileName)


    def WndProc(self, message):
       if message.Value.Msg == CLIPBOARD_DRAW:
           self.onPaste(None, None)
       Form.WndProc(self, message)
       
       
    def initTabControl(self):
        self.tabControl = TabControl(
            Dock = DockStyle.Fill,
            Alignment = TabAlignment.Bottom
        )
        self.Controls.Add(self.tabControl)


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
        toolBar = ToolStrip(
            Dock = DockStyle.Top
        )

        def addToolBarIcon(pickledIcon, name, clickHandler):
            button = ToolStripButton()
            if pickledIcon:
                button.Image = loads(pickledIcon)
            button.ImageTransparentColor = Color.Magenta
            button.ToolTipText = button.Name = name
            button.DisplayStyle = ToolStripItemDisplayStyle.Image
            if clickHandler:
                button.Click += clickHandler
            toolBar.Items.Add(button)

        addToolBarIcon(OpenIcon, "Open", self.onOpen)
        addToolBarIcon(SaveIcon, "Save", self.onSave)
        addToolBarIcon(CloseIcon, "Close", self.onClose)
        addToolBarIcon(CopyIcon, "Copy", self.onCopy)
        addToolBarIcon(PasteIcon, "Paste", self.onPaste)
        addToolBarIcon(ViewIcon, "Image mode", self.onImageMode)

        self.Controls.Add(toolBar)


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
        openFileDialog = OpenFileDialog(
            Filter = FILTER,
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:
            for fileName in openFileDialog.FileNames:
                self.openFile(fileName)


    def openFile(self, fileName):
        image = self.getImage(fileName)
        if image:
            self.createTab(image, fileName)


    def onClose(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            self.tabControl.TabPages.Remove(selectedTab)
            del self.paths[self.tabControl.SelectedIndex]


    def onCopy(self, _, __):
        dataObject = DataObject()
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            dataObject.SetImage(selectedTab.Controls[0].image)
            Clipboard.SetDataObject(dataObject)


    def onPaste(self, _, __):
        dataObject = Clipboard.GetDataObject()
        if dataObject.ContainsImage():
            self.createTab(dataObject.GetImage())


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
        if selectedTab:
            if len(selectedTab.Controls):
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


Application.EnableVisualStyles()
Application.Run(MainForm())
