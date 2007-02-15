# Image Pickle Example
# (c) 2007 Andrzej Krzywda, Christian Muirhead & Michael Foord
# email: fuzzyman AT voidspace DOT org DOT uk
# web:   http://www.voidspace.org.uk/ironpython/
#

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import cPickle as pickle
import fepy_pickle
from System.Drawing import Bitmap

from System.Windows.Forms import (
    Application, DockStyle, Form, PictureBox
)


fepy_pickle.register(Bitmap)

image = Bitmap('fuzzyman.bmp')
imageString = pickle.dumps(image, 0)


del image


form = Form(Text="Fuzzyman")
pictureBox = PictureBox()
pictureBox.Dock = DockStyle.Fill

newImage = pickle.loads(imageString)

pictureBox.Image = newImage
form.Controls.Add(pictureBox)

Application.Run(form)

