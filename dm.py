"""
Database module
for inventory program
Angus Goody
09/01/2020
"""


#-----------Imports----------

#-----------Functions----------

#-----------Classes----------

class dataBase:
    """
    The dataBase
    is used to store
    categories or items
    """
    def __init__(self,dbName):
        self.name=dbName
        self.categories={} #Store categories
        self.items={} #Store items
        self.validTemplates=[clothingTemplate] #Store valid templates

    def addCategory(self,catName):
        """
        Will add a category to the
        database
        """
        if catName not in self.categories:
            newCat=dbCategory(catName)
            self.categories[catName]=newCat

    def addItem(self,itemName,**kwargs):
        """
        Will add an item to the database
        the optional parameter is category
        "cat" = category
        """
        cat=kwargs.get("cat")
        if cat in self.categories:
            self.categories[cat].addItem(itemName)
        else:
            #Create an item
            newItem=dbItem(itemName)
            #Store it
            self.items[itemName]=newItem

    def addTemplate(self,itemName,templateClass):
        """
        Create a item with a template
        already
        """
        if templateClass in self.validTemplates:
            #Create the template
            newTemplate=templateClass(itemName)
            #Store
            self.items[itemName]=newTemplate
        else:
            print("Invalid template")


    def displayStr(self,**kwargs):
        """
        Display all data
        """
        currentLevel=kwargs.get("level",0)
        indent="    "*(currentLevel)
        print(indent,"======"+str(self.name)+"======")
        #Display Items
        for item in self.items:
            self.items[item].displayStr(level=currentLevel)
        #Display Categories
        for cat in self.categories:
            self.categories[cat].displayStr(level=currentLevel+1)

    
    def getIndentedCatNames(self,**kwargs):
        """
        Return an array of names with appropriate indentation
        """
        currentLevel=kwargs.get("level",-1)
        indent="   "*(currentLevel)
        newArray=[]
        #Add self
        if currentLevel > -1:
            newArray.append([indent+str(self.name),self])
        #Add children
        for cat in self.categories:
            allNames=self.categories[cat].getIndentedCatNames(level=currentLevel+1)
            for i in allNames:
                print(i)
                newArray.append(i)
        return newArray
        
    def getCategory(self,catName):
        """
        Return category object
        """
        if catName in self.categories:
            return self.categories[catName]


class dbCategory(dataBase):
    """
    A category is a way
    to further organise
    contents of the db
    """
    def __init__(self,catName):
        dataBase.__init__(self,catName)


class dbItem:
    """
    A dbItem is the
    actual data in the inventory
    ie. laptop etc
    """
    def __init__(self,itemName):
        #Preset Fields
        self.itemName=itemName
        self.fields=[] #Store array of field objects
        self.fieldNames=[] #Store names of all fields


    def addField(self,fieldName,fieldType):
        """
        Add a field to the item
        *Text
        *Number
        *Currency
        *Paragraph
        """
        if fieldName not in self.fieldNames:
            self.fieldName.append(fieldName)
            newField=None
            if fieldType == "Number":
                newField=dbItemNumberField(fieldName)
            elif fieldType == "Currency":
                newField=dbItemCurrencyField(fieldName)
            elif fieldType == "Paragraph":
                newField=dbItemParagraphField(fieldName)
            else:
                newField=dbItemTextField(fieldName)

            #Store
            self.fields.append(newField)

    def displayStr(self,**kwargs):
        """
        Display the item
        """
        currentLevel=kwargs.get("level",0)
        indent="    "*(currentLevel)
        print(indent,"*",self.itemName)
class dbItemField:
    """
    The dbItemField
    is a class for each
    field of an item
    ie. Name, price etc
    """
    def __init__(self,name,dataType):
        self.name=name
        self.dataType=dataType
        self.storedData=None


#-----------Field Templates----------

class dbItemTextField(dbItemField):
    """
    Field element for a plain
    text
    """
    def __init__(self,name):
        dbItemField.__init__(self,name,"Text")
        self.storedData=""

class dbItemNumberField(dbItemField):
    """
    Field element for integer or decimal
    """
    def __init__(self,name):
        dbItemField.__init__(self,name,"Number")
        self.storedData=0

class dbItemCurrencyField(dbItemField):
    """
    Field element for integer or decimal
    """
    def __init__(self,name):
        dbItemField.__init__(self,name,"Currency")
        self.currency="£"
        self.storedData=0

class dbItemParagraphField(dbItemField):
    """
    Field element for integer or decimal
    """
    def __init__(self,name):
        dbItemField.__init__(self,name,"Paragraph")
        self.storedData=""

#-----------Item Templates----------

class clothingTemplate(dbItem):
    """
    Template for storing
    an item of clothing
    """
    def __init__(self,name):
        dbItem.__init__(self,name)
        #Add templates
        self.addField("Brand","Text")
        self.addField("Purchase Date","Text")
        self.addField("Purchase Price","Currency")
        self.addField("Value","Currency")