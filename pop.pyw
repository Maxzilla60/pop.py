import random, webbrowser, sys, os
import tkinter as tk
from tkinter import filedialog
from winsound import PlaySound, SND_FILENAME

class Pop(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initExceptionCallback()
        self.hideWindow()
        self.windowSetup()
        self.getFileName()
        self.getSessionFromFile()
        self.uiSetup()
        self.setDefaultURL()
        self.updateWindowTitle()
        self.showWindow()

    def pop(self):
        if self.sessionIsEmpty():
            return
        self.getNewURL()
        self.updateCountLabel()
        webbrowser.open(self.url)
        PlaySound('pop.wav', SND_FILENAME)
        self.updateFileContents()

    def initExceptionCallback(self):
        self.parent.report_callback_exception = self.report_callback_exception

    def report_callback_exception(self, exc, val, tb):
        from tkinter import messagebox
        from string import Template
        err = Template("$exc\n$tb\n\n$val").safe_substitute(exc=str(exc), val=str(val), tb=str(tb))
        messagebox.showerror("Whoops, an Exception!", err)

    def getFileName(self):
        if len(sys.argv) >= 2:
            file = sys.argv[1]
        else:
            file = filedialog.askopenfilename(initialdir = ".", initialfile="url_list.txt", title = "Pop Random URL - Select session file", filetypes = (("text files","*.txt"),("all files","*.*")))
            if not file:
                sys.exit()
        self.file = file

    def getSessionFromFile(self):
        with open(self.file) as sessionFile:
            self.session = sessionFile.readlines()

    def setDefaultURL(self):
        self.updateURL("Click Pop! (or press P)")

    def windowSetup(self):
        self.parent.iconbitmap(default='pop.ico')
        self.parent.title("Pop Random URL")
        self.parent.bind("<P>", lambda event: self.pop())
        self.parent.bind("<p>", lambda event: self.pop())
        self.parent.bind("<Escape>", lambda event: sys.exit())
        self.alwaysOnTop()

    def alwaysOnTop(self):
        self.parent.attributes("-topmost", True)

    def uiSetup(self):
        self.urlLabelSetup()
        self.countLabelSetup()
        self.checkBoxSetup()
        self.buttonSetup()

    def urlLabelSetup(self):
        self.urlLabel = tk.Text(self.parent, height=1, font=('Consolas', 12))
        self.urlLabel.pack(fill=tk.X)

    def countLabelSetup(self):
        self.countLabel = tk.Label(self.parent, text=len(self.session), font=('Ubuntu', 16), fg="blue")
        self.countLabel.pack(fill=tk.X)

    def checkBoxSetup(self):
        self.noDelete = tk.IntVar()
        self.noDelete.set(0)
        self.checkBox = tk.Checkbutton(self.parent, text="Don't delete", font=('Ubuntu', 12), variable=self.noDelete, onvalue=1, offvalue=0)
        self.checkBox.pack(fill=tk.X)

    def buttonSetup(self):
        self.button = tk.Button(self.parent, text='Pop!', height=2, font=('Ubuntu', 20, 'bold'), command=lambda: self.pop())
        if self.sessionIsEmpty():
            self.button.config(state=tk.DISABLED)
        self.button.pack(fill=tk.X)

    def updateWindowTitle(self):
        self.parent.title("Pop Random URL - " + self.file)

    def updateURL(self, newURL):
        self.url = newURL
        self.urlLabel.delete(1.0, tk.END)
        self.urlLabel.insert(tk.END, self.url)

    def updateCountLabel(self):
        self.countLabel.config(text=str(len(self.session)))
        if self.sessionIsEmpty():
            self.button.config(state=tk.DISABLED)

    def sessionIsEmpty(self):
        return len(self.session) <= 0


    def getNewURL(self):
        i = random.randrange(0, len(self.session))
        if self.noDeleteEnabled():
            choice = self.session[i].rstrip()
        else:
            choice = self.session.pop(i).rstrip()
        self.updateURL(choice)

    def noDeleteEnabled(self):
        return self.noDelete.get()

    def updateFileContents(self):
        with open(self.file, 'w') as sessionFile:
            for line in self.session:
                sessionFile.write("%s" % line)

    def hideWindow(self):
        self.parent.withdraw()

    def showWindow(self):
        self.parent.deiconify()

root = tk.Tk()

if (sys.version_info < (3, 0)):
    from tkinter import messagebox
    root.withdraw()
    messagebox.showerror("Python 2 detected", "This program requires Python 3 or higher")
elif __name__ == "__main__":
    Pop(root).pack(side="top", fill="both", expand=True)
    root.mainloop()