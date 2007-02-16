using System;
using System.IO;
using System.Windows.Forms;
using IronPython.Hosting;
using IronPython.Runtime;

namespace TabbedImages {
    
    class TabbedImages {

        [STAThread]
        static void Main(string[] args) {

            PythonEngine engine = new PythonEngine();
            engine.AddToPath(Path.GetDirectoryName(Application.ExecutablePath));
            engine.Sys.argv = List.Make(args);
            string path = Path.Combine(Path.GetDirectoryName(Application.ExecutablePath), "main.py");
            engine.ExecuteFile(path);

        }
    }
}
