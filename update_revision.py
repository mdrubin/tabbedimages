# creates revision.py with the output of svnversion

from System.Diagnostics import Process

contents = '__revision__ = "%s"\n'

p = Process()
p.StartInfo.UseShellExecute = False
p.StartInfo.RedirectStandardOutput = True
p.StartInfo.FileName = "svnversion"
p.Start()
p.WaitForExit()
revision = p.StandardOutput.ReadToEnd()

output = open("revision.py", "w")
output.write(contents % revision.strip())
output.close()

