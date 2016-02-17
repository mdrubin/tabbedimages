A very simple [IronPython](http://www.codeplex.com/IronPython) application. IronPython is an implementation of Python for the dotnet platform.

The Tabbed Image Viewer can view multiple images, in tabpages, and save images in different formats. It can copy images to the clipboard, and paste images from the clipboard into a new tab. It also supports drag and drop and has a clipboard viewer (will auto-paste images from the clipboard into a new tab - useful for screenshots). All in 500 lines of IronPython code.

Created as a simple demo of IronPython and Windows Forms, for [PyCon 2007](http://us.pycon.org/).

It is tested on Windows, and although it works on Mono there are minor issues.

There is a package available for download, including all the source files, and a Windows executable. (The .NET framework 2.0 redistributable must be installed.)

Alternatively, the whole project can be obtained with Subversion.

There is a sample Visual Studio project (C#) which is a simple example of embedding the IronPython engine (for IronPython 1) to create a custom executable, plus an example of extending IronPython with a C# class.

By: Andrzej Krzywda, Christian Muirhead and Michael Foord.