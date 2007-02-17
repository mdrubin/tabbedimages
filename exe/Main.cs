using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;
using IronPython.Hosting;
using IronPython.Runtime;

namespace TabbedImages {
    
    class TabbedImages {

        [STAThread]
        static void Main(string[] rawArgs) {
            List<string> args = new List<string>(rawArgs);
            args.Insert(0, Application.ExecutablePath);

            PythonEngine engine = new PythonEngine();
            engine.AddToPath(Path.GetDirectoryName(Application.ExecutablePath));
            engine.Sys.argv = List.Make(args);

            EngineModule engineModule = engine.CreateModule("__main__",  new Dictionary<string, object>(), true);
            engine.DefaultModule = engineModule;
            
            string path = Path.Combine(
                Path.GetDirectoryName(Application.ExecutablePath), "main.py");
            engine.ExecuteFile(path);

        }
    }
}
