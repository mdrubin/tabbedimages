# Tabbed Image Viewer
# (c) 2007 Andrzej Krzywda, Christian Muirhead & Michael Foord
# email: fuzzyman AT voidspace DOT org DOT uk
# web:   http://www.voidspace.org.uk/ironpython/
#

from System.Windows.Forms import (
    Button, DialogResult, DockStyle, Form, FormBorderStyle
)


class AboutDialog(Form):

    def __init__(self):
        Form.__init__(self)

        self.okButton = Button()
        self.okButton.Text = "OK"
        self.okButton.Dock = DockStyle.Bottom | DockStyle.Right
        self.okButton.Parent = self
        self.okButton.Click += self.onOK

        self.AcceptButton = self.okButton

        self.Text = "About"

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MinimizeBox = False
        self.MaximizeBox = False


    def onOK(self, _, __):
        self.DialogResult = DialogResult.OK

