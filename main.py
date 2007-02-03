import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Bitmap
from System.Windows.Forms import (
    Application, DockStyle, Form, MenuStrip, 
    OpenFileDialog, PictureBox, PictureBoxSizeMode, 
    TabControl, TabAlignment, 
    TabPage, ToolStripMenuItem    
)
from System.IO import Path


NO_IMAGE = 'No Image'

class MainForm(Form):
    
    def __init__(self):
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        
        self.initTabs()
        self.initMenu()
        

    def initTabs(self):
        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Bottom
        
        page = TabPage()
        page.Text = NO_IMAGE
        self.tabControl.TabPages.Add(page)
        
        self.Controls.Add(self.tabControl)
        
    
    def initMenu(self):
        menuStrip = MenuStrip()
        menuStrip.Name = "Main MenuStrip"
        menuStrip.Dock = DockStyle.Top
        
        fileMenu = ToolStripMenuItem()
        fileMenu.Name = 'File Menu'
        fileMenu.Text = '&File'
        
        openMenuItem = ToolStripMenuItem()
        openMenuItem.Name = 'Open'
        openMenuItem.Text = '&Open...'
        openMenuItem.Click += self.onOpen
        fileMenu.DropDownItems.Add(openMenuItem)
        
        menuStrip.Items.Add(fileMenu)
        
        self.Controls.Add(menuStrip)
        

    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog()
        openFileDialog.ShowDialog()
        tabPage = self.tabControl.TabPages[0]
        if tabPage.Text != NO_IMAGE:
            tabPage = TabPage()
            self.tabControl.TabPages.Add(tabPage)
            self.tabControl.SelectedTab = tabPage
        tabPage.Text = Path.GetFileName(openFileDialog.FileName)
        pictureBox = PictureBox()

        image = Bitmap(openFileDialog.FileName)
        pictureBox.Image = image
        pictureBox.ClientSize = image.Size
               
        tabPage.Controls.Clear()
        tabPage.Controls.Add(pictureBox)
        

Application.EnableVisualStyles()
Application.Run(MainForm())