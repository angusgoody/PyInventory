
"""
Python Inventory software
Angus Goody
6/01/20
"""

#---------Imports--------

from shed.colourTools import *
from shed.storageTools import *
from shed.tkinterTools import *
from dm import *


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
        self.buttonBar.addButton("Exit")
        self.buttonBar.addButton("Create")
        self.buttonBar.addButton("Open")
     
class dbHomeScreen(screen):
    """
    Where the user 
    is first taken
    when opening a database
    """
    def __init__(self,controller):
        screen.__init__(self,controller,"View")
        #Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        #Top Bar
        self.topBar=mainFrame(self)
        self.topBar.grid(row=0,column=0)
        self.topBar.gridConfig(0)
        #Label
        self.titleVar=StringVar()
        self.titleVar.set("Viewing Database")
        self.titleLabel=Label(self.topBar,textvariable=self.titleVar,font=globalFontMega)
        self.titleLabel.grid(row=0,column=0,pady=6)
        #Center Frame
        self.centerFrame=mainFrame(self)
        self.centerFrame.grid(row=1,column=0)
        self.centerFrame.gridConfig(0)
        self.addItemButton=Button(self.centerFrame,text="Add Item",width=globalButtonWidth)
        self.addItemButton.grid(row=0,column=0,pady=5)
        self.addCategoryButton=Button(self.centerFrame,text="Add Category",width=globalButtonWidth)
        self.addCategoryButton.grid(row=1,column=0,pady=5)
        self.viewAllButton=Button(self.centerFrame,text="View All",width=globalButtonWidth)
        self.viewAllButton.grid(row=2,column=0,pady=5)
        #Button Bar
        self.buttonBar=buttonSection(self)
        self.buttonBar.grid(row=2,column=0)
        self.buttonBar.addButton("Back")


#---------Popups--------

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
        self.buttonBar.addButton("Cancel")
        self.buttonBar.addButton("Save")
        #Add exit button command
        self.buttonBar.getButton("Cancel").config(command=self.quit)

    def setup(self):
        #Before launching find existing names to add to banned words
        bannedWords=[]
        allFilenames=self.master.projectManager.findAllUserFiles()
        for item in allFilenames:
            bannedWords.append(getBasename(getFileWithoutExtension(item)))
        print("Banned words",bannedWords)
        #Add banned words
        self.databaseNameSection.entry.bannedWords=bannedWords
        #Config Buttons
        self.buttonBar.getButton("Save").config(command=lambda: 
            self.master.checkNewDatabaseName(self))

class addItemWindow(mainTopLevel):
    """
    When the user clicks
    "add item" this window
    will popup
    """
    def __init__(self,windowInstance):
        mainTopLevel.__init__(self,windowInstance,"Add Item")
        #Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)
        #Variables
        self.currentCat=None #The category the user chose
        self.currentTemplate=None #Template user chose
        #Center
        self.centerFrame=mainFrame(self)
        self.centerFrame.grid(row=0,column=0)
        #Add data sections
        self.databaseNameSection=dataSection(self.centerFrame,"Item Name:"+" "*2)
        self.databaseNameSection.grid(row=0,column=0,pady=15)
        #Select Category
        self.categorySection=optionMenuSection(self.centerFrame,"Category: "+" "*2)
        self.categorySection.grid(row=1,column=0,pady=15)
        #Select Template
        self.templateSection=optionMenuSection(self.centerFrame,"Template: "+" "*2)
        self.templateSection.grid(row=2,column=0,pady=15)
        #Add Button Bar
        self.buttonBar=buttonSection(self)
        self.buttonBar.grid(row=1,column=0)
        self.buttonBar.addButton("Cancel")
        self.buttonBar.addButton("Save")
        #Add exit button command
        self.buttonBar.getButton("Cancel").config(command=self.quit)

    def updateCategory(self,catInstance):
        """
        Will update the text for the
        option menu and store the object
        kwargs can be used to specify
        if the instance is the default (None)
        """
        #Store
        self.currentCat=catInstance
        if type(catInstance) is dataBase:
            self.categorySection.optionVar.set("None")
        else:
            #Add the cat to the display
            self.categorySection.optionVar.set(catInstance.name)

    def updateTemplate(self,name,tmpInstance):
        """
        Will update the text for the optionMenu
        displaying the template
        """
        #Store
        self.currentTemplate=tmpInstance
        #Update the text
        self.templateSection.optionVar.set(name)


    def loadContents(self,currentDB,templateManager):
        """
        Will use the currentDB object
        to load the contents of the
        window
        """
        #--------Adding categories--------
        #Clear the menu
        optMenu=self.categorySection.optionMenu.children["menu"]
        optMenu.delete(0,"end")
        #Add the None option
        optMenu.add_command(label="None",
            command=lambda o=currentDB:self.updateCategory(o))

        #Setup the None category as default if user picks nothing
        self.updateCategory(currentDB)
        #Add a seperator
        optMenu.insert_separator(1)
        #Get all child categories and add commands
        catArray=currentDB.getIndentedCatNames()
        #Add themy to the optionMenu
        for item in catArray:
            display=item[0]
            obj=item[1]
            optMenu.add_command(label=display,
                command=lambda o=obj: self.updateCategory(o))

        #--------Adding templates--------
        tmpMenu=self.templateSection.optionMenu.children["menu"]
        tmpDict=templateManager.templateDict
        tmpMenu.delete(0,"end")
        #Find the valid templates (None is included in class dict)
        for t in tmpDict:
            display=t
            obj=tmpDict[t]
            #Add the command using lambda
            tmpMenu.add_command(label=display,
                command=lambda o=obj,n=display: self.updateTemplate(n,o))
            #Add the seperator after None
            if display == "None":
                tmpMenu.insert_separator(1)

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
        #Store globals
        self.currentDB=None
        self.templateManager=templateManager()


        #----------Instances---------
        #Screen Instances
        self.startScreen=startScreen(self.screenMaster)
        self.startScreen.show()
        self.dbHomeScreen=dbHomeScreen(self.screenMaster)

        #----------Commands---------
        #-----Start Screen-----
        self.startScreen.buttonBar.getButton("Exit").config(command=self.exitProgram)
        self.startScreen.buttonBar.getButton("Create").config(command=self.launchCreateDatabaseWindow)
        self.startScreen.buttonBar.getButton("Open").config(command=self.attemptOpenDatabase)
        #-----DBHome-----
        self.dbHomeScreen.buttonBar.getButton("Back").config(command=self.closeDatabase)
        self.dbHomeScreen.addItemButton.config(command=self.launchAddItemWindow)
        #self.dbHomeScreen.addCategoryButton.config(command=self.laun)

        #----------Last Calls---------
        
        self.loadAllUserDatabases()

        #----------testing---------
        """
        newDb=dataBase("Bagggz")
        newDb.addCategory("Electronics")
        newDb.addItem("Macbook",cat="Electronics")
        newDb.addItem("iPad",cat="Electronics")
        elCat=newDb.getCategory("Electronics")
        elCat.addCategory("Phones")
        elCat.addItem("iPhone xs Max",cat="Phones")
        elCat.addItem("Blackberry Bold",cat="Phones")
        elCat.addItem("Nexus 5",cat="Phones")

        newDb.addCategory("Hats")
        newDb.addItem("P6 Logo Trucker",cat="Hats")
        newDb.addItem("Gore Tex new era",cat="Hats")


        newDb.addCategory("Bags")
        newDb.addItem("Patagonia Black Hole 25l",cat="Bags")
        newDb.addItem("The North Face Borealis",cat="Bags")
        newDb.addItem("Fjallraven raven 20l",cat="Bags")
        newDb.addItem("Thule Bag",cat="Bags")

        newDb.displayStr()
        self.projectManager.saveUserData("BagData",newDb)

        print("Finished and saved")
        """
    def loadAllUserDatabases(self):
        """
        Will locate user data
        """
        data=self.projectManager.loadAllUserFiles()
        #Clear the listbox
        self.startScreen.listbox.clear()
        for name in data:
            obj=data[name]
            #If the file name has been changed externally
            if obj.name != name:
                name=str(name)+" ("+str(obj.name)+")"
            self.startScreen.listbox.addObject(name,obj)

    def checkNewDatabaseName(self,windowObject):
        """
        Will check the name the user
        entered is valid, create it
        and then load the screen
        """
        advancedEntryObject=windowObject.databaseNameSection.entry
        validOrNot=advancedEntryObject.contentValid
        content=advancedEntryObject.getContent()
        if validOrNot:
            #Create and save the new db
            newDb=self.createNewDatabase(content)
            #Close the popup
            windowObject.quit()
            #Open the new database
            print("Ready to open")
            self.displayDatabase(newDb)

        else:
            reason=advancedEntryObject.reasonInvalid
            showMessage("Error",reason)

    def createNewDatabase(self,name):
        """
        Will create a new database
        given a name
        """
        newDb=dataBase(name)
        #Store
        self.projectManager.saveUserData(name,newDb)
        return newDb

    def displayDatabase(self,dataBaseObject):
        """
        Will take datbase as parameter
        and display it on the screen
        """
        self.dbHomeScreen.show()
        #Update Vars
        displayText="Database: "+str(dataBaseObject.name)
        self.dbHomeScreen.titleVar.set(displayText)
        self.currentDB=dataBaseObject

    #---------Lambda Functions----------

    #---------Button Commands----------

    def launchCreateDatabaseWindow(self):
        """
        Launches a window
        for the user to create a new database
        """
        #Create our new popup
        newWindow=createDatabaseWindow(self)
        newWindow.setup()
        newWindow.runWindow()

    def launchAddItemWindow(self):
        """
        Will launch the popup window
        to allow users to "add item"
        """
        newWindow=addItemWindow(self)
        newWindow.loadContents(self.currentDB,self.templateManager)
        newWindow.runWindow()

    def attemptOpenDatabase(self):
        """
        Called when user clicks
        the "Open" button on start screen
        """
        #Get object from listbox
        current=self.startScreen.listbox.getCurrentObject()
        if current:
            self.displayDatabase(current)
        else:
            showMessage("Error","Please select a database or create one")

    def closeDatabase(self):
        """
        Called when user clicks "quit"
        """
        self.loadAllUserDatabases()
        self.startScreen.show()


    def exitProgram(self):
        """
        Will exit the prorgam
        """
        self.destroy()
if __name__ == '__main__':
    window=inventoryWindow()
    window.mainloop()