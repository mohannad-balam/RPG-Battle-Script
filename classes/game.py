import random
from .magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self,name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxHp = hp
        self.hp = hp
        self.maxMp = mp
        self.mp = mp
        self.atkL = atk - 10
        self.atkH = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["attack", "magic", "items"]

    def generateDmg(self):
        return random.randrange(self.atkL, self.atkH)

    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def heal(self, amount) : 
        self.hp += amount
        if self.hp > self.maxHp :
            self.hp = self.maxHp
        # return self.hp    

    def getHp(self):
        return self.hp

    def getMaxHp(self):
        return self.maxHp

    def getMp(self):
        return self.mp

    def getMaxMp(self):
        return self.maxMp

    def reduceMp(self, cost):
        self.mp -= cost

    def getSpellName(self, i):
        return self.magic[i]["name"]

    def getSpellMpCost(self, i):
        return self.magic[i]["cost"]

    def chooseAction(self):
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name +"'s " + "turn :" + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD +"    ACTIONS : " + bcolors.ENDC)
        for item in self.actions:
            print(str(i) + ".", item)
            i += 1

    def chooseMagic(self):
        i = 1
        print("\n"+ bcolors.OKBLUE + bcolors.BOLD + "    MAGIC : " + bcolors.ENDC)
        for spell in self.magic :
            print("         "+ str(i) + ".", spell.name, "(cost : ",str(spell.cost) + ")")
            i += 1
        print("         " + str(0) + "." + " [go back]")

    def chooseItem(self) : 
        i = 1
        print("\n"+ bcolors.OKGREEN + bcolors.BOLD + "    ITEMS : " + bcolors.ENDC)
        for item in self.items : 
            print("         "+ str(i) + ".", str(item["item"].name), ":", str(item["item"].descreption), "(x"+ str(item["quantity"]) +")")
            i += 1
        print("         " + str(0) + "." + " [go back]")
    
    def chooseTarget(self, enemies) :
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET : " + bcolors.ENDC)
        for enemy in enemies :
            if enemy.getHp() != 0 :
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    choose a target : ")) - 1
        return choice
    #_________________________________________________________
     
    #getiing enemeis stats
    def getEnemyStats(self) :
        #hp bar logic 
        hpBar = ""
        hpTicks = ((self.hp / self.maxHp) * 100) / 2
        
        while hpTicks > 0 :
            hpBar += "█"
            hpTicks -= 1
        #end while
        
        while len(hpBar) < 50 :
            hpBar += " "
        #end while    
        #__________________________________

        hpString = str(self.hp) + "/" + str(self.maxHp)
        currentHp = ""
        
        #that means there is decrement
        if len(hpString) < 11 :
            #storing how many characters have been decreased
            decreased = 11 - len(hpString)
            #___________________________
            while decreased > 0 :
                currentHp += " "
                decreased -= 1
            currentHp += hpString
        else:
            #if there is no decrementation
            currentHp = hpString        
        #_______________________________________________
        
        print("                                __________________________________________________")
        print(bcolors.BOLD + self.name +"            "+ currentHp + "|"+ bcolors.FAIL + hpBar +bcolors.ENDC + bcolors.BOLD+"|")    
    
    
    #getting players stats
    def getStats(self) :
        
        #hp bar logic 
        hpBar = ""
        hpTicks = ((self.hp / self.maxHp) * 100) / 4
        
        while hpTicks > 0 :
            hpBar += "█"
            hpTicks -= 1
        #end while
        
        while len(hpBar) < 25 :
            hpBar += " "
        #end while    
        #__________________________________
        
        #mp bar logic 
        mpBar = ""
        mpTicks = ((self.mp / self.maxMp) * 100) / 10
        
        while mpTicks > 0 :
            mpBar += "█"
            mpTicks -= 1
        #end while
        
        while len(mpBar) < 10 :
            mpBar += " "
        #end while
        #_____________________________________  
        
        hpString = str(self.hp) + "/" + str(self.maxHp)
        currentHp = ""
        
        #that means there is decrement
        if len(hpString) < 9 :
            #storing how many characters have been decreased
            decreased = 9 - len(hpString)
            #___________________________
            while decreased > 0 :
                currentHp += " "
                decreased -= 1
            currentHp += hpString
        else:
            #if there is no decrementation
            currentHp = hpString        
        #_______________________________________________
        
        
        mpString = str(self.mp) + "/" + str(self.maxMp)  
        currentMp = ""
        
        if len(mpString) < 7 :
            decreased = 7 - len(mpString)
            while decreased > 0 :
                currentMp += " "
                decreased -= 1
            currentMp += mpString
            
        else:
            currentMp = mpString
            
                
        print("                              _________________________            __________")
        print(bcolors.BOLD + self.name +"            "+ currentHp + "|"+ bcolors.OKGREEN + hpBar +bcolors.ENDC + bcolors.BOLD+"|     "+mpString+"|" + bcolors.OKBLUE+ mpBar+ bcolors.ENDC+"|")
    
    def chooseEnemySpell(self) :
        magicChoice = random.randrange(0, len(self.magic))
        spell = self.magic[magicChoice]
        spellDamage = spell.generateSpellDamage()   
        
        if self.mp < spell.cost :
            #recursion
            self.chooseEnemySpell() 
        else :
            return spell, spellDamage    