import clr
clr.AddReference('System.Windows.Forms')

from System.Windows.Forms import (Application, DockStyle, Form, MenuStrip, TabControl, 
    TabAlignment, TabPage, ToolStripMenuItem
)


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
        page.Text = 'No Image'
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
        openMenuItem.Text = '&Open'
        fileMenu.DropDownItems.Add(openMenuItem)
        
        menuStrip.Items.Add(fileMenu)
        
        self.Controls.Add(menuStrip)
        

    def openImage(self):
        pass

Application.EnableVisualStyles()
Application.Run(MainForm())