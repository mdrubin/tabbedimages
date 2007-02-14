using System;
using IronPython.Hosting;

namespace TabbedImages {
    
    class TabbedImages {

        [STAThread]
        static void Main(string[] args) {

            PythonEngine engine = new PythonEngine();
            engine.AddToPath(".");
            engine.ExecuteFile("main.py");

        }
    }
}
