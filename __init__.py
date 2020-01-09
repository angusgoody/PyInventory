
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
        self.buttonBar=buttonSection(self)
        self.buttonBar.grid(row=2,column=0)
        self.buttonBar.addButton("Create")
        self.buttonBar.addButton("Open")
        

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
        self.databaseNameSection=dataSection(self.centerFrame,"Database Name: ")
        self.databaseNameSection.grid(row=0,column=0)
        #Add Button Bar
        self.buttonBar=buttonSection(self)
        self.buttonBar.grid(row=1,column=0)
        self.buttonBar.addButton("Quit")
        self.buttonBar.addButton("Save")


#---------Other Classes--------

class tempDatabase:
    def __init__(self,name):
        self.name=name
        self.age=10
        self.myList=["angus","goody"]

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
        #Project manager setup
        self.projectManager=projectManager(getWorkingDirectory(),"inventory")
        self.projectManager.fileExtension=".inv"


        #----------Instances---------
        #Screen Instances
        self.startScreen=startScreen(self.screenMaster)
        self.startScreen.show()


        #----------Commands---------
        #-----Home Screen-----
        self.startScreen.buttonBar.getButton("Create").config(command=self.launchCreateDatabaseWindow)

        #----------Testing---------
        #self.tempDB=tempDatabase("harry")
        #self.projectManager.saveUserData("harry",self.tempDB)
        self.loadAllUserDatabases()

    def loadAllUserDatabases(self):
        """
        Will locate user data
        """
        data=self.projectManager.findAllUserFiles()
        #Add objects to the listbox
        
    
    def launchCreateDatabaseWindow(self):
        """
        Launches a window
        for the user to create a new database
        """
        newWindow=createDatabaseWindow(self)
        newWindow.runWindow()
        #Config Buttons
        newWindow.buttonBar.getButton("Quit").config(command=lambda: newWindow.quit())
        newWindow.buttonBar.getButton("Save").config(command=lambda: 
            self.checkNewDatabaseName(newWindow.databaseNameSection.entry))

    def checkNewDatabaseName(self,advancedEntryObject):
        """
        Will check the name the user
        entered is valid
        """
        validOrNot=advancedEntryObject.contentValid
        if validOrNot:
            print("Ready to create database")
        else:
            reason=advancedEntryObject.reasonInvalid
            showMessage("Error",reason)


    def createNewDatabase(self,name):
        """
        Will create a new database
        """
        pass

if __name__ == '__main__':
    window=inventoryWindow()
    window.mainloop()