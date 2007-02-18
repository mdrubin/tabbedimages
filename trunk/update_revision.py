# creates revision.py with the output of svnversion

from System import DateTime
from System.Diagnostics import Process

date = DateTime.Now.ToString().split()[0]
contents = '__revision__ = "Build %s.    %s"\n'

p = Process()
p.StartInfo.UseShellExecute = False
p.StartInfo.RedirectStandardOutput = True
p.StartInfo.FileName = "svnversion"
p.Start()
p.WaitForExit()
revision = p.StandardOutput.ReadToEnd()

output = open("revision.py", "w")
output.write(contents % (revision.strip(), date))
output.close()

