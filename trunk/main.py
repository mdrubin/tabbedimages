import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from icons import CopyIcon
from cPickle import loads
from System import ArgumentException
from System.Drawing import Bitmap, Color
from System.Windows.Forms import (
    Application, Clipboard, DataObject, DialogResult, 
    DockStyle, Form, ImageList, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, PictureBox, PictureBoxSizeMode, 
    TabControl, TabAlignment, 
    TabPage, ToolBar, ToolBarButton, ToolStripMenuItem    
)
from System.IO import Path


class MainForm(Form):
    
    def __init__(self):
        Form.__init__(self)
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        
        self.initTabControl()
        self.initToolBar()
        self.initMenu()
        

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
        closeMenuItem = self.createMenuItem('Close', '&Close', self.onClose)
        exitMenuItem  = self.createMenuItem('Exit', 'E&xit', lambda *_: Application.Exit())
        
        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(closeMenuItem)   
        fileMenu.DropDownItems.Add(exitMenuItem)
        
        editMenu = self.createMenuItem('Edit Menu', '&Edit')
        copy =  self.createMenuItem('Copy', '&Copy', self.onCopy)
        paste = self.createMenuItem('Paste', '&Paste', self.onPaste)
        editMenu.DropDownItems.Add(copy)
        editMenu.DropDownItems.Add(paste)
        
        menuStrip.Items.Add(fileMenu)
        menuStrip.Items.Add(editMenu)
        
        self.Controls.Add(menuStrip)

    
    def initToolBar(self):
        toolBar = ToolBar(
            Dock = DockStyle.Top
        )
        imageList = ImageList()
        imageList.TransparentColor = Color.White
        copyIcon = loads(CopyIcon)
        
        imageList.Images.Add(copyIcon)
        toolBar.ImageList = imageList
        copyButton = ToolBarButton()
        copyButton.ImageIndex = 0
        toolBar.Buttons.Add(copyButton)
        self.Controls.Add(toolBar)
        
        
    def getImage(self, fileName):        
        try:
            return Bitmap(fileName)
        except ArgumentException:
            MessageBox.Show(fileName + " doesnt't appear to be a valid image file", 
                            "Invalid image format",
                            MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
            return None
    
    
    def getPictureBox(self, image):    
        return PictureBox(
            Dock = DockStyle.Fill,
            Image = image,                
            SizeMode = PictureBoxSizeMode.StretchImage
        )
        
        
    def createTab(self, image, label):        
        tabPage = TabPage()
        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage
        tabPage.Text = label
        pictureBox = self.getPictureBox(image)
        tabPage.Controls.Add(pictureBox)        
            
            
    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog(
            Filter = "Images (*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*",
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:                
            for fileName in openFileDialog.FileNames:                                
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
        
        
Application.EnableVisualStyles()
Application.Run(MainForm())