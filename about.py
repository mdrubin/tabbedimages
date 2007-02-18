# Tabbed Image Viewer
# (c) 2007 Andrzej Krzywda, Christian Muirhead & Michael Foord
# email: fuzzyman AT voidspace DOT org DOT uk
# web:   http://www.voidspace.org.uk/ironpython/
#

from System.Drawing import Bitmap, Point
from System.IO import Path
from System.Windows.Forms import (
    Button, DialogResult, DockStyle, Form, FormBorderStyle, Label, PictureBox
)

try:
    from revision import __revision__
except ImportError:
    __revision__ = "generate version info"


def loadImage(root, name):
    return Bitmap.FromFile(Path.Combine(root, name))


class AboutDialog(Form):

    def __init__(self, imagePath):
        Form.__init__(self)

        self.Width = 346
        self.Height = 215

        self.images = dict((name, loadImage(imagePath, name + '.jpg'))
            for name in ('pycon', 'andrzej', 'michael', 'christian'))

        self.pictureBox = PictureBox()
        self.pictureBox.Parent = self
        self.pictureBox.Location = Point(234, 12)
        self.pictureBox.TabStop = False
        self.switchImage("pycon")

        self.mainText = Label()
        self.mainText.Parent = self
        self.mainText.AutoSize = True
        self.mainText.Location = Point(12, 12);
        self.mainText.Text = ("Tabbed Image Viewer\r\n\r\nWritten for PyCon 2007\r\n"
                              "Using IronPython and Windows Forms\r\n\r\nBy:")

        self.addNameLabel("Andrzej Krzywda", "andrzej", Point(36, 90))
        self.addNameLabel("Christian Muirhead", "christian", Point(36, 105))
        self.addNameLabel("Michael Foord", "michael", Point(36, 120))

        versionLabel = Label()
        versionLabel.Parent = self
        versionLabel.AutoSize = True
        versionLabel.Location = Point(12, 151)
        versionLabel.Text = "Version: " + __revision__

        self.okButton = Button()
        self.okButton.Parent = self
        self.okButton.Text = "OK"
        self.okButton.Location = Point(251, 146)
        self.okButton.Click += self.onOK

        self.AcceptButton = self.okButton

        self.Text = "About"

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MinimizeBox = False
        self.MaximizeBox = False


    def onOK(self, _, __):
        self.DialogResult = DialogResult.OK


    def addNameLabel(self, name, imageName, location):
        label = Label()
        label.Parent = self
        label.AutoSize = True
        label.Location = location
        label.Text = name
        label.MouseEnter += lambda *_: self.switchImage(imageName)
        label.MouseLeave += self.resetImage


    def switchImage(self, name):
        self.pictureBox.Image = self.images[name]
        self.pictureBox.Size = self.images[name].Size


    def resetImage(self, sender, eventArgs):
        self.switchImage("pycon")


