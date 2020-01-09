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