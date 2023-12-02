import random
from classes.magic import Spell


class bcolors:
  HEADER = "\033[95m"
  OKBLUE = "\033[94m"
  OKGREEN = "\033[92m"
  WARNING = "\033[93m"
  FAIL = "\033[91m"
  ENDC = "\033[0m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"


class Character:

  def __init__(self, name, hp, mp, attack, defence, magic, items) -> None:
    self.name = name
    self.max_hp = hp
    self.hp = hp
    self.max_mp = mp
    self.mp = mp
    self.attk_low = attack - 10
    self.attk_high = attack + 10
    self.df = defence
    self.magic = magic
    self.items = items
    self.actions = ["ATTACK", "MAGIC", "ITEMS"]

  def generate_damage(self):
    return random.randrange(self.attk_low, self.attk_high)

  def take_damage(self, dmg):
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0
    return self.hp

  def reduce_mp(self, cost):
    self.mp -= cost

  def choose_action(self):
    index_number = 1
    print("\n" + bcolors.BOLD + str(self.name) + ": " + bcolors.ENDC)
    print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
    for item in self.actions:
      print(f"        {index_number}: {item}")
      index_number += 1

  def choose_magic(self):
    index_number = 1
    print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
    for spell in self.magic:
      print(
          "   " + str(index_number) + ":",
          spell.name,
          "(cost:" + str(spell.cost) + ")",
      )
      index_number += 1

  def choose_items(self):
    index_number = 1
    print(bcolors.OKBLUE + bcolors.BOLD + "    ITEMS: " + bcolors.ENDC)
    for item in self.items:
      print(
          f"    \n{index_number}: {item['item'].name}:: {item['item'].description} , x{item['quantity']}"
      )
      index_number += 1

  def heal(self, dmg):
    self.hp += dmg
    if self.hp > self.max_hp:
      self.hp = self.max_hp

  def get_hp(self):
    return self.hp

  def get_max_hp(self):
    return self.max_hp

  def get_mp(self):
    return self.mp

  def get_max_mp(self):
    return self.max_mp

  def get_enemy_stats(self):
    hp_bar = ""
    bar_ticks = (self.hp / self.max_hp) * 100 / 2

    while bar_ticks > 0:
      hp_bar += "█"
      bar_ticks -= 1
    while len(hp_bar) < 50:
      hp_bar += " "

    hp_string = f"{self.hp}/{self.max_hp}"
    current_hp = ""
    if len(hp_string) < 11:
      decreased = 11 - len(hp_string)
      while decreased > 0:
        current_hp += " "
        decreased -= 1
      current_hp += hp_string
    else:
      current_hp = hp_string
    print("                           Enemy HP")
    print(
        "                           __________________________________________________"
    )
    print(
        f"{self.name}:      {current_hp} {bcolors.FAIL}|{hp_bar}|{bcolors.ENDC}"
    )

  def choose_target(self, enemies):
    i = 1
    print(f"\n{bcolors.FAIL}{bcolors.BOLD}    TARGET:{bcolors.ENDC}")
    for enemy in enemies:
      if enemy.get_hp() != 0:
        print(f"        {i}. {enemy.name}")
        i += 1
    choice = int(input("    Choose target: ")) - 1
    return choice

  def get_stats(self):
    hp_bar = ""
    bar_ticks = (self.hp / self.max_hp) * 100 / 4

    mp_bar = ""
    mp_ticks = (self.mp / self.max_mp) * 100 / 10

    while bar_ticks > 0:
      hp_bar += "█"
      bar_ticks -= 1
    while len(hp_bar) < 25:
      hp_bar += " "

    while mp_ticks > 0:
      mp_bar += "█"
      mp_ticks -= 1
    while len(mp_bar) < 10:
      mp_bar += " "

    hp_string = f"{self.hp}/{self.max_hp}"
    current_hp = ""
    if len(hp_string) < 9:
      decreased = 9 - len(hp_string)
      while decreased > 0:
        current_hp += " "
        decreased -= 1
      current_hp += hp_string
    else:
      current_hp = hp_string

    mp_string = f"{self.mp}/{self.max_mp}"
    current_mp = ""
    if len(mp_string) < 7:
      decreased = 7 - len(mp_string)
      while decreased > 0:
        current_mp += " "
        decreased -= 1
      current_mp += mp_string
    else:
      current_mp = mp_string
    print(
        "                       _________________________                __________"
    )
    print(
        f"{self.name}:      {current_hp} {bcolors.OKGREEN}|{hp_bar}|{bcolors.ENDC}      {current_mp} {bcolors.OKBLUE}|{mp_bar}|{bcolors.ENDC}"
    )
    print()
