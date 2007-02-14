using System;
using System.IO;
using System.Windows.Forms;
using IronPython.Hosting;

namespace TabbedImages {
    
    class TabbedImages {

        [STAThread]
        static void Main(string[] args) {

            PythonEngine engine = new PythonEngine();
            engine.AddToPath(Path.GetDirectoryName(Application.ExecutablePath));
            engine.ExecuteFile("main.py");

        }
    }
}
