import clr
clr.AddReference("System.Windows.Forms")
from System.Threading import Thread
from System.Windows.Forms import (DialogResult, DragDropEffects,
    Form, OpenFileDialog)
from main import MainForm
import unittest


def assertTabPages(form, expectedNumber):
    assert len(form.Controls["TabControl"].TabPages) == expectedNumber
    
class OpenFilesTest(unittest.TestCase):
    
    def testUsesRealOpenFileDialog(self):
        form = MainForm()
        self.assertTrue(isinstance(form.openFileDialog, OpenFileDialog))
        
    def testFreshFormHasEmptyTabControl(self):
        form = MainForm()
        assertTabPages(form, 0)
        
    def testFreshFormOpensFilesCancelledHasEmptyTabControl(self):
        openFileDialog=MockOpenFileDialog(
            DialogResult = DialogResult.Cancel)
        form = MainForm(openFileDialog)
        form.onOpen(None, None)
        assertTabPages(form, 0)
        
    def testFreshFormOpensFiles(self):       
        openFileDialog=MockOpenFileDialog(
            DialogResult = DialogResult.OK,
            FileNames = ["images\\andrzej.jpg", 
                         "images\\michael.jpg"])
        form = MainForm(openFileDialog)
        form.onOpen(None, None)
        assertTabPages(form, 2)


       
class Event(object):
    def __init__(self, containsFiles, files=None):
        self.Data = MockDataObject(containsFiles, files)
        self.Effect = None
        
class MockDataObject(object):
    def __init__(self, containsFiles, files=None):
        self.containsFiles = containsFiles
        if files: self.files = files
    def ContainsFileDropList(self):
        return self.containsFiles
    def GetFileDropList(self):
        return self.files
    
class DragFilesTest(unittest.TestCase):
        
    def testDragNonFilesEffect(self):
        form = MainForm()
        assert form.AllowDrop
        event = Event(containsFiles=False)
        form.onDragEnter(None, event)
        assert event.Effect == DragDropEffects.None        
        
    def testDragFilesEffect(self):
        form = MainForm()
        event = Event(containsFiles = True)
        form.onDragEnter(None, event)
        assert event.Effect == DragDropEffects.Copy
        
    def testDragDropFiles(self):
        form = MainForm()
        fileNames = ["images\\andrzej.jpg", 
                     "images\\michael.jpg"]
        event = Event(containsFiles=True, files=fileNames)
        form.onDragDrop(None, event)
        assertTabPages(form, 2)
        
        
        
class MockOpenFileDialog(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def ShowDialog(self):
        return self.DialogResult


class MockFileOpenDialogTest(unittest.TestCase):        
    
    def testGetOpenFileDialog(self):
        mockOpenDialog = MockOpenFileDialog(
            Multiselect = True,
            Filter = "All files (*.*)|*.*"
        )
        assert mockOpenDialog.Multiselect == True
        assert mockOpenDialog.Filter == "All files (*.*)|*.*"
        
        
    def testShowDialogReturnsResult(self):
        arg1 = object()
        mockOpenDialog = MockOpenFileDialog(
            DialogResult = arg1
        )
        self.assertEquals(mockOpenDialog.ShowDialog(), arg1)
        
        
    def testFilenames(self):
        l = ["1", "2", "3"]
        mockOpenDialog = MockOpenFileDialog(
            Filenames = l
        )
        self.assertEquals(mockOpenDialog.Filenames, l)
        
if __name__ == "__main__":
    unittest.main()
    