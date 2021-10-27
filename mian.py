from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#github user name : mohannad-balam

# print("\n\n")
# print("NAME                       HP                                    MP")

# player1
# print("                              _________________________             __________")
# print(bcolors.BOLD + "Williams:            480/480 |"+ bcolors.OKGREEN +"█████████████████████████" +bcolors.ENDC + bcolors.BOLD+"|     65/65 |" + bcolors.OKBLUE+"██████████"+bcolors.ENDC+"|")
# player2
# print("                              _________________________             __________")
# print(bcolors.BOLD + "HattoriH:            480/480 |"+ bcolors.OKGREEN +"█████████████████████████" +bcolors.ENDC + bcolors.BOLD+"|     65/65 |" + bcolors.OKBLUE+"██████████"+bcolors.ENDC+"|")
# player3
# print("                              _________________________             __________")
# print("Tokugawa Eiasu:      480/480 |█████████████████████████|     65/65 |██████████|")


#creating balck magic
fire = Spell("Fire", 21, 140, "black")
thunder = Spell("Thunder", 31, 280, "black")
blizzard = Spell("BLizzard", 19, 108, "black")
meteor = Spell("Meteor", 45, 460, "black")
quake = Spell("Quake", 13, 120, "black")
#-------------------------------------------


#creating some items
potion = Item("potion", "potion", "restore 120 HP" , 120)
hiPotion = Item("HiPotion" , "potion" , "restore 300 HP", 300)
megaPotion = Item("MegaPotion", "potion" , "restore 1200 HP", 1200)
elixer = Item("elixer", "elixer", "fully restore HP/MP for a party member" , 9999)
megaElixer = Item("MegaElixer", "elixer" , "fully restore all Party's HP/MP", 9999)
#---------------------------------------------
grenade = Item("grenade", "attack", "Deals 500 damage", 500)
#---------------------------------------------

#crearing white magic
cure = Spell("cure", 21, 200, "white")
Hcure = Spell("hiCure", 32, 420, "white")
#--------------------------------------------

playerMagic = [fire, thunder, blizzard, meteor, quake, cure, Hcure]
enemyMagic = [fire, meteor, cure]
playerItems = [
    {"item": potion, "quantity": 15},
    {"item": hiPotion, "quantity": 8},
    {"item": megaPotion, "quantity": 5},
    {"item": elixer, "quantity": 7},
    {"item": megaElixer, "quantity": 3},
    {"item": grenade, "quantity": 4},
]

#instantiate people
player1 = Person("Noctis: ",2480, 65, 191, 54, playerMagic, playerItems)
player2 = Person("Ignis:  ",2176, 82, 121, 42, playerMagic, playerItems)
player3 = Person("Gladio: ",3292, 53, 154, 87, playerMagic, playerItems)
player4 = Person("Prompto:",1592, 59, 87, 34, playerMagic, playerItems)

players = [player1, player2, player3, player4]

enemy1 = Person("Goblin  ", 1250, 76, 560, 45, enemyMagic, [])
enemy2 = Person("Ifrit   ",11500, 85, 542, 64, enemyMagic, [])
enemy3 = Person("Goblin  ", 1250, 76, 560, 45, enemyMagic, [])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "\n" + "''''''''''''ENCOUNTER!''''''''''''" + bcolors.ENDC)
    
#Looping the entire battle    
while running :
    print("==============================")
    
    print("\n\n")
    print("NAME                          HP                                   MP")
    #getting the player stats each time the actions were finished
    for player in players :
        player.getStats()
    print("\n")
    
    #getting the enemies stats
    for enemy in enemies :
        enemy.getEnemyStats()
    
    #looping the entire party allowing them to take part in battle
    for player in players :
        
        player.chooseAction()
        choice = input("    Choose Action : ")
        index = int(choice) - 1
        
        #attacking logic
        if index == 0 :
            dmg = player.generateDmg()
            #we're gonna return the target enemy's index and store into a variable in order to use it in the list
            enemyTarget = player.chooseTarget(enemies)
            #when we chose the enemy we wanna attack let's put it into the index of the list of enemies
            enemies[enemyTarget].takeDamage(dmg)
            print("You Attacked", enemies[enemyTarget].name.replace(" ", ""), "For",dmg,"Points of Damage.")
            
            #if the enemy died we're gonna remove him from the list and keep going
            if enemies[enemyTarget].getHp() == 0 :
                print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemyTarget].name.replace(" ", "") + "Has Died!" + bcolors.ENDC)
                del enemies[enemyTarget]
        elif index == 1:
            player.chooseMagic()
            magicChoice = int(input("    Chooce a spell :")) - 1
            
            #a way to go back a menu
            if magicChoice == -1 :
                continue
            #-----------------------
            
            spell = player.magic[magicChoice]
            spellDmg = spell.generateSpellDamage()
            #==========================
            currentMp = player.getMp()
            
            if spell.cost > currentMp :
                print(bcolors.FAIL + "\n===Not Enough MP===\n" + bcolors.ENDC)
                continue
            
            player.reduceMp(spell.cost)
            
            if spell.type == "white" :
                player.heal(spellDmg)
                print(bcolors.OKBLUE + "\n" + spell.name,"Heals",spellDmg,"HP.\n" + bcolors.ENDC)
            elif spell.type == "black" :
                enemyTarget = player.chooseTarget(enemies)
                #when we chose the enemy we wanna attack let's put it into the index of the list of enemies
                enemies[enemyTarget].takeDamage(spellDmg)
                print("\n" + bcolors.OKBLUE + spell.name ,"Deals", str(spellDmg) ,"Points Of Damage On", enemies[enemyTarget].name.replace(" ", ""), bcolors.ENDC + "\n")
                
                if enemies[enemyTarget].getHp() == 0 :
                    print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemyTarget].name.replace(" ", "") + "Has Died!" + bcolors.ENDC)
                    del enemies[enemyTarget]
        
        elif index == 2 :
            player.chooseItem()
            itemChoice = int(input("    Choose Item : ")) - 1  
            
            # a way to go back a menu
            if itemChoice == -1 :
                continue  
            #-----------------------
            
            #stroing the item we've chosen into a variable
            item = player.items[itemChoice]["item"]
            #--------------------------------
            
            #checkihg if the item we wanna use not = to zero
            if player.items[itemChoice]["quantity"] == 0 :
                print(bcolors.FAIL + "=========EMPTY=========" + bcolors.ENDC)
                continue
            
            #reducing the item quantity by 1 each time you used one
            player.items[itemChoice]["quantity"] -= 1
            
            if item.type == "potion" :
                player.heal(item.proberty)
                print(bcolors.OKGREEN + "\n" + item.name, "Heals for", str(item.proberty), "HP" + bcolors.ENDC)
            elif item.type == "elixer" :
                #mega elixer fluuy restores all the party's hp and mp
                if item.name == "MegaElixer" :
                    for i in players :
                        i.hp = i.maxHp
                        i.mp = i.maxMp
                #___________________________________   
                else : 
                    #one elixer fully restores a player hp and mp   
                    player.hp = player.maxHp
                    player.mp = player.maxMp
                print(bcolors.OKGREEN + "\n" + item.name, "Fully restored HP/MP." + bcolors.ENDC)    
            elif item.type == "attack" :
                enemyTarget = player.chooseTarget(enemies)
                #when we chose the enemy we wanna attack let's put it into the index of the list of enemies
                enemies[enemyTarget].takeDamage(item.proberty)
                print(bcolors.FAIL + "\n" + item.name, "Deals", str(item.proberty), "Points of damage On", enemies[enemyTarget].name.replace(" ", "") + bcolors.ENDC)
            
                if enemies[enemyTarget].getHp() == 0 :
                    print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemyTarget].name.replace(" ", "") + " Has Died!" + bcolors.ENDC)
                    del enemies[enemyTarget]
    defeatedEnemies = 0
    defeatedPlayers = 0
    
    for enemy in enemies :
        if enemy.getHp() == 0 :
            defeatedEnemies += 1
    
    for player in players :
        if player.getHp() == 0 :
            defeatedPlayers += 1        
    
    if defeatedEnemies == enemies.count :
        print("\n" + bcolors.OKGREEN + "============You Won!============" + bcolors.ENDC + "\n")
        running = False

    elif defeatedPlayers == players.count :
        print(bcolors.OKGREEN + "============YOU DIED!============" + bcolors.ENDC)
        running = False
    
    #enemy attack phase
    for enemy in enemies :
        #we're generatig indexes between 0 and 2 because rn enemy cant't choose [items]
        enemyChoice = random.randrange(0, 2)
        
        if enemyChoice == 0 :
            #that means he's gonna be atacking us
            target = random.randrange(0,4)
            #generate a random number allowing the enemy to choose who is to attack
            enemyDmg = enemy.generateDmg()
            players[target].takeDamage(enemyDmg)
    
            #displaying how much damage he dealt
            print("\n"+ enemy.name.replace(" ", "") +" Attacked "+ players[target].name +" For",enemyDmg,"Points of Damage.\n")
            print("-------------------------------------")

        elif enemyChoice == 1 :
            #that means he's gonna use magic
            spell , spellDamage = enemy.chooseEnemySpell()
            enemy.reduceMp(spell.cost)
            
            
            if spell.type == "white" :
                enemy.heal(spellDmg)
                print(bcolors.OKBLUE + "\n" + spell.name,"Heals",enemy.name.replace(" ", ""),spellDmg,"HP.\n" + bcolors.ENDC)
            elif spell.type == "black" :
                playerTarget = random.randrange(0,4)
                #when we chose the enemy we wanna attack let's put it into the index of the list of enemies
                players[playerTarget].takeDamage(spellDmg)
                print("\n" + bcolors.OKBLUE + enemy.name.replace(" ", "")+ "'s " + spell.name ,"Deals", str(spellDmg) ,"Points Of Damage On", players[playerTarget].name.replace(" ", ""), bcolors.ENDC + "\n")
                
                if players[playerTarget].getHp() == 0 :
                    print("\n" + bcolors.FAIL + bcolors.BOLD + players[playerTarget].name.replace(" ", "") + " Has Died!" + bcolors.ENDC)
                    del players[playerTarget]
                    
                    
            print("Enemy Chose", spell.name, "damage is", str(spellDamage))
    
    defeatedEnemies = 0
    defeatedPlayers = 0
    
    for enemy in enemies :
        if enemy.getHp() == 0 :
            defeatedEnemies += 1
    
    for player in players :
        if player.getHp() == 0 :
            defeatedPlayers += 1        
    
    if defeatedEnemies == enemies.count :
        print("\n" + bcolors.OKGREEN + "============You Won!============" + bcolors.ENDC + "\n")
        running = False

    elif defeatedPlayers == players.count :
        print(bcolors.OKGREEN + "============YOU DIED!============" + bcolors.ENDC)
        running = False
    
    
    # elif player.getHp() == 0 :
    #     print(bcolors.FAIL + "===You Died!===" + bcolors.ENDC)   
    #     running = False
