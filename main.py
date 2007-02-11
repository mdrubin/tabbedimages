import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import ArgumentException
from System.Drawing import Bitmap
from System.Windows.Forms import (
    Application, DialogResult, DockStyle, Form, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, PictureBox, PictureBoxSizeMode, 
    TabControl, TabAlignment, 
    TabPage, ToolBar, ToolStripMenuItem    
)
from System.IO import Path


class MainForm(Form):
    
    def __init__(self):
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        
        self.initTabControl()
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
            print clickHandler
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
        menuStrip.Items.Add(fileMenu)
        
        
        self.Controls.Add(menuStrip)

    
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
        
        
    def createTab(self, fileName):
        image = self.getImage(fileName)
        if not image:
            return
        
        tabPage = TabPage()
        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage
        tabPage.Text = Path.GetFileName(fileName)
        pictureBox = self.getPictureBox(image)
        tabPage.Controls.Add(pictureBox)        
            
            
    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog(
            Filter = "Images (*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*",
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:                
            for fileName in openFileDialog.FileNames:
                self.createTab(fileName)
        
        
    def onClose(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            self.tabControl.TabPages.Remove(selectedTab)
        
        
Application.EnableVisualStyles()
Application.Run(MainForm())