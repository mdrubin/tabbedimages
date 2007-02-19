using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace Clipboard
{
    public class Clipboard
    {
        [DllImport("User32.dll", CharSet = CharSet.Auto)]
        public static extern IntPtr SetClipboardViewer(IntPtr hWndNewViewer);
    }
}
