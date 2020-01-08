
"""
Python Inventory software
Angus Goody
6/01/20
"""

#---------Imports--------

from shed.colourTools import *
from shed.storageTools import *
from shed.tkinterTools import *



#---------Screens--------

class startScreen(screen):
    """
    The Programs startScreen
    """
    def __init__(self,controller):
        screen.__init__(self,controller,"Home")
        #Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        #Top Bar
        self.topBar=mainFrame(self)
        self.topBar.grid(row=0,column=0)
        self.topBar.gridConfig(0)
        #Label
        self.titleLabel=Label(self.topBar,text="Select or create database",font=globalFontBig)
        self.titleLabel.grid(row=0,column=0,pady=6)
        #Listbox
        self.listbox=advancedListbox(self)
        self.listbox.grid(row=1,column=0,sticky="NSEW")
        #Bottom Bar
        self.bottomBar=mainFrame(self)
        self.bottomBar.grid(row=2,column=0)
        self.bottomBar.gridConfig(0)
        self.bottomButtonBar=mainFrame(self.bottomBar)
        self.bottomButtonBar.grid(row=0,column=0,pady=20)
        #Add Buttons
        self.createButton=Button(self.bottomButtonBar,text="Create",width=globalButtonWidth)
        self.createButton.grid(row=0,column=0,padx=10)
        self.openButton=Button(self.bottomButtonBar,text="Open",width=globalButtonWidth)
        self.openButton.grid(row=0,column=1,padx=10)

class createDatabaseWindow(mainTopLevel):
    """
    A popup window
    that will allow the user
    to create a new database
    """
    def __init__(self,windowInstance):
        mainTopLevel.__init__(self,windowInstance,"Create Database")
        #Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)
        #Center
        self.centerFrame=mainFrame(self)
        self.centerFrame.grid(row=0,column=0)
        #Add data sections
        self.databaseNameSection=dataSection(self.centerFrame,"Name: ")
        self.databaseNameSection.grid(row=0,column=0)


#---------Main Program--------

class inventoryWindow(Tk):
    """
    The class for the main inventory
    program
    """
    def __init__(self):
        Tk.__init__(self)
        #Setup
        self.title("Inventory")
        self.geometry("700x600")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.screenMaster=screenController(self)
        self.screenMaster.grid(row=0,column=0,sticky="NSEW")

        #----------Instances---------
        #Screen Instances
        self.startScreen=startScreen(self.screenMaster)
        self.startScreen.show()
        #TopLevel Instances
        self.createDatabaseWindow=createDatabaseWindow(self)

        #----------Commands---------
        #-----Home Screen-----
        self.startScreen.createButton.config(command=self.launchCreateDatabaseWindow)


    def launchCreateDatabaseWindow(self):
        """
        Launches a window
        for the user to create a new database
        """
        self.createDatabaseWindow.runWindow()



if __name__ == '__main__':
    window=inventoryWindow()
    window.mainloop()