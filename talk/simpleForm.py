import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Application, Button, Form

form = Form()
form.Text = 'Hello World'

button = Button(Text='Click Me')
form.Controls.Add(button)

clr.AddReference('System.Drawing')
from System.Drawing import Point
x = y = 0
def onClick(sender, event):
   global x, y
   x += 15
   y += 15
   button.Location = Point(x, y)

button.Click += onClick

Application.Run(form)