from classes.game import Character, bcolors
from classes.magic import Spell
from classes.inventory import Item
from random import randrange

# Create Black Magic
fire = Spell("Fire", 25, 600, "Black")
thunder = Spell("Thunder", 25, 600, "Black")
blizzard = Spell("Blizzard", 25, 600, "Black")
meteor = Spell("Meteor", 40, 1200, "Black")
quake = Spell("Quake", 14, 140, "Black")

# Create White Magic
cure = Spell("Cure", 25, 620, "White")
cura = Spell("Cura", 32, 1500, "White")

# Create some item
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super-potion", "potion", "Heals 1000 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member",
              9999)
hi_elixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spell = [fire, meteor, cure]
player_items = [
    {
        "item": potion,
        "quantity": 15
    },
    {
        "item": hi_potion,
        "quantity": 5
    },
    {
        "item": super_potion,
        "quantity": 5
    },
    {
        "item": elixir,
        "quantity": 3
    },
    {
        "item": hi_elixir,
        "quantity": 1
    },
    {
        "item": grenade,
        "quantity": 3
    },
]

player1 = Character("Valos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Character("Nick ", 4160, 188, 300, 34, player_spells, player_items)
player3 = Character("John ", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Character("Imp    ", 1250, 130, 560, 325, enemy_spell, [])
enemy2 = Character("Antonio", 11200, 701, 525, 25, enemy_spell, [])
enemy3 = Character("Imp    ", 1250, 130, 560, 325, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!" + bcolors.ENDC)
while running:
  print("====================")
  print("\n\n")
  print("NAME                   HP                                       MP")
  for player in players:
    player.get_stats()
  print("\n")

  for enemy in enemies:
    enemy.get_enemy_stats()
  for player in players:
    player.choose_action()
    choice = input("    Choose action: ")
    index = int(choice) - 1
    if index == 0:
      dmg = player.generate_damage()
      enemy = player.choose_target(enemies)
      enemies[enemy].take_damage(dmg)
      print(f"You hit {enemies[enemy].name.strip()} for {dmg}")

      if enemies[enemy].get_hp() == 0:
        print(f"{enemies[enemy].name.strip()} has died")
        del enemies[enemy]
    elif index == 1:
      player.choose_magic()
      magic_choice = int(input("    Choose magic: ")) - 1
      if magic_choice == -1:
        continue
      spell = player.magic[magic_choice]
      magic_dmg = spell.generate_damage()

      current_mp = player.get_mp()
      if spell.cost > current_mp:
        print(bcolors.FAIL + "\nNot enough magic point" + bcolors.ENDC + "\n")
        continue
      player.reduce_mp(spell.cost)
      if spell.type == "White":
        player.heal(magic_dmg)
        print(
            bcolors.OKBLUE + "\n" + spell.name + "heals for",
            str(magic_dmg),
            "HP." + bcolors.ENDC,
        )
      elif spell.type == "Black":
        enemy = player.choose_target(enemies)
        enemies[enemy].take_damage(magic_dmg)
        print(
            bcolors.OKBLUE + "\n" + spell.name + "deals ",
            str(magic_dmg),
            "points of damage to " + enemies[enemy].name.strip() +
            bcolors.ENDC,
        )
        if enemies[enemy].get_hp() == 0:
          print(f"{enemies[enemy].name} has died")
          del enemies[enemy]
    elif index == 2:
      player.choose_items()
      item_choice = int(input("    Choose item: ")) - 1
      print()
      if item_choice == -1:
        continue
      item = player.items[item_choice]["item"]
      if player.items[item_choice]["quantity"] == 0:
        print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
        continue
      player.items[item_choice]["quantity"] -= 1

      if item.type == "potion":
        player.heal(item.prop)
        print(
            bcolors.OKGREEN + "\n" + item.name + " heals for",
            str(item.prop) + " HP" + bcolors.ENDC,
        )
      elif item.type == "elixir":
        if item.name == "MegaElixir":
          for i in players:
            i.hp = player.max_hp
            i.mp = player.max_mp
        else:
          player.hp = player.max_hp
          player.mp = player.max_mp
        print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" +
              bcolors.ENDC)
      elif item.type == "attack":
        enemy = player.choose_target(enemies)
        enemies[enemy].take_damage(item.prop)
        print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) +
              " points of damage to" + enemies[enemy].name.strip() +
              bcolors.ENDC)
        if enemies[enemy].get_hp() == 0:
          print(f"{enemies[enemy].name.strip()} has died")
          del enemies[enemy]

# check if battle is over
  defeated_enemies = 0
  defeated_players = 0
  for enemy in enemies:
    if enemy.get_hp() == 0:
      defeated_enemies += 1

  for player in players:
    if player.get_hp() == 0:
      defeated_players += 1
# check if player won
  if defeated_enemies == 2:
    print(bcolors.OKGREEN + "You win!!" + bcolors.ENDC)
    running = False
# check if enemy won
  elif defeated_players == 2:
    print(f"{bcolors.FAIL}Your enemies have defeated you{bcolors.ENDC}")
    running = False

  for enemy in enemies:
    enemy_choice = randrange(0, 2)
    if enemy_choice == 0:
      # chose attack
      target = randrange(0, len(players))
      enemy_dmg = enemy.generate_damage()
      players[target].take_damage(enemy_dmg)
      print(
          f"{enemy.name.strip()} attacks {players[target].name.strip()} for {enemy_dmg}"
      )
    elif enemy_choice == 1:
      magic_choice = randrange(0, len(enemy.magic))
      spell = enemy.magic[magic_choice]
      magic_dmg = spell.generate_damage()

      pct = enemy.hp / enemy.max_hp * 100
      if enemy.mp < spell.cost:
        continue

      enemy.reduce_mp(spell.cost)

      if spell.type == "White":
        enemy.heal(magic_dmg)
        print(
            bcolors.OKBLUE + "\n" + spell.name +
            f" heals {enemy.name.strip()} for",
            str(magic_dmg),
            "HP." + bcolors.ENDC,
        )
      elif spell.type == "Black":
        target = randrange(0, 3)
        players[target].take_damage(magic_dmg)
        print("\n" + enemy.name.strip() + " " + spell.name + " deals",
              str(magic_dmg),
              "points of damage to " + players[target].name.strip())
        if players[target].get_hp() == 0:
          print(f"{players[target].name.strip()} has died")
          del players[target]
