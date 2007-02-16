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
    OpenIcon, PasteIcon, SaveIcon
)

from cPickle import loads
from System import ArgumentException
from System.Drawing import Bitmap, Color
from System.Drawing.Imaging import ImageFormat
from System.Windows.Forms import (
    Application, Clipboard, ContextMenuStrip, DataObject, DialogResult,
    DockStyle, Form, ImageList, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, PictureBox, PictureBoxSizeMode,
    SaveFileDialog, TabControl, TabAlignment,
    TabPage, ToolStrip, ToolStripButton,
    ToolStripMenuItem, ToolStripItemDisplayStyle
)
from System.IO import Path

FILTER = "Images (*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*"

class MainForm(Form):

    def __init__(self):
        Form.__init__(self)
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200

        self.initTabControl()
        self.initToolBar()
        self.initMenu()
        self.initContextMenu()
        
        for fileName in sys.argv[1:]:
            self.openFile(fileName)


    def initTabControl(self):
        self.tabControl = TabControl(
            Dock = DockStyle.Fill,
            Alignment = TabAlignment.Bottom
        )
        self.Controls.Add(self.tabControl)


    def createMenuItem(self, name, text, clickHandler=None):
        menuItem = ToolStripMenuItem(
            Name = name,
            Text = text
        )
        if clickHandler:
            menuItem.Click += clickHandler
        return menuItem


    def initMenu(self):
        menuStrip = MenuStrip(
            Name = "Main MenuStrip",
            Dock = DockStyle.Top
        )
        fileMenu      = self.createMenuItem('File Menu', '&File')
        openMenuItem  = self.createMenuItem('Open', '&Open...', self.onOpen)
        saveMenuItem  = self.createMenuItem('Save', '&Save...', self.onSave)
        closeMenuItem = self.createMenuItem('Close', '&Close', self.onClose)
        exitMenuItem  = self.createMenuItem('Exit', 'E&xit', lambda *_: Application.Exit())

        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(saveMenuItem)
        fileMenu.DropDownItems.Add(closeMenuItem)
        fileMenu.DropDownItems.Add(exitMenuItem)

        editMenu = self.createMenuItem('Edit Menu', '&Edit')
        copy =  self.createMenuItem('Copy', '&Copy', self.onCopy)
        paste = self.createMenuItem('Paste', '&Paste', self.onPaste)
        view = self.createMenuItem('View Mode', '&View Mode', self.onImageMode)
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
        addToolBarIcon(None, "Image mode", self.onImageMode)

        self.Controls.Add(toolBar)


    def getImage(self, fileName):
        try:
            return Bitmap(fileName)
        except ArgumentException:
            MessageBox.Show(fileName + " doesn't appear to be a valid image file",
                            "Invalid image format",
                            MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
            return None


    def getPictureBox(self, image, mode=PictureBoxSizeMode.StretchImage):
        keyWArgs = {'Image': image,
                    'SizeMode': mode}
        if mode == PictureBoxSizeMode.StretchImage:
            keyWArgs['Dock'] = DockStyle.Fill
        return PictureBox(**keyWArgs)


    def createTab(self, image, label):
        tabPage = TabPage()
        tabPage.Text = label
        pictureBox = self.getPictureBox(image)
        tabPage.Dock = DockStyle.Fill
        tabPage.AutoScroll = True
        tabPage.Controls.Add(pictureBox)

        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage


    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog(
            Filter = FILTER,
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:
            for fileName in openFileDialog.FileNames:
                self.openFile(fileName)
                
    
    def openFile(self, fileName):
        h = open('test.txt', 'a')
        h.write(fileName + '\n')
        try:
            import os
            h.write(str(os.path.isfile(fileName)) + '\n')
            h.write(os.getcwd() + '\n')
        except:
            pass
        h.close()
        image = self.getImage(fileName)
        if image:
            self.createTab(image, Path.GetFileName(fileName))


    def onClose(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            self.tabControl.TabPages.Remove(selectedTab)


    def onCopy(self, _, __):
        dataObject = DataObject()
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            dataObject.SetImage(selectedTab.Controls[0].Image)
            Clipboard.SetDataObject(dataObject)


    def onPaste(self, _, __):
        dataObject = Clipboard.GetDataObject()
        if dataObject.ContainsImage():
            self.createTab(dataObject.GetImage(), "CLIPBOARD")


    def onSave(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            image = selectedTab.Controls[0].Image
            saveFileDialog = SaveFileDialog()
            saveFileDialog.Filter = FILTER
            if saveFileDialog.ShowDialog() == DialogResult.OK:
                extension = Path.GetExtension(saveFileDialog.FileName)
                fileName = saveFileDialog.FileName
                format = ImageFormat.Jpeg
                if extension.lower() == "bmp":
                    format = ImageFormat.Bmp
                elif extension.lower() == "gif":
                    format = ImageFormat.Gif
                else:
                    if not (fileName.lower().endswith('jpg')
                            or fileName.lower().endswith('jpeg')):
                        fileName += '.jpg'
                    format = ImageFormat.Jpeg
                    
                image.Save(saveFileDialog.FileName, format)


    def onAbout(self, _, __):
        AboutDialog().ShowDialog()
        
        
    def onImageMode(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            if selectedTab.Controls:
                currentMode = selectedTab.Controls[0].SizeMode
                image = selectedTab.Controls[0].Image
                selectedTab.Controls.RemoveAt(0)
                if currentMode == PictureBoxSizeMode.AutoSize:
                    selectedTab.Controls.Add(self.getPictureBox(image, 
                                                                PictureBoxSizeMode.StretchImage))
                else:
                    selectedTab.Controls.Add(self.getPictureBox(image, 
                                                                PictureBoxSizeMode.AutoSize))


Application.EnableVisualStyles()
Application.Run(MainForm())
