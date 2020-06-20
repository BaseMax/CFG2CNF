# Author: Max Base
# Date: 2020/06/17
# Web: maxbase.org
# Repo: https://github.com/BaseMax/CFG2CNF
import sys
print("Enter your grammers with `S -> ab` similar style, Also you can split grammers by | and even write grammers in diffrent lines\nand finaly type *:")
moves={}
rules={}
# alphas=list(map(chr, range(97, 123)))
alphas=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
while True:
  line=input()
  if line == "*":
    break
  parts=line.split("->")
  parts[0]=parts[0].strip()
  parts[1]=parts[1].strip()
  parts[1]=parts[1].split("|")
  # print(parts)
  if not parts[0] in rules:
    rules[parts[0]]=[]
  for part in parts[1]:
    part=part.strip()
    # print(part)
    rules[parts[0]].append(part)

def new_name_for_grammer(array):
  names=list(array)
  # print(names)
  for alpha in alphas:
    if alpha not in names:
      return alpha
  print("Error: cannot find a new and fresh name for new Grammer statement!")
  sys.exit(-1)

def delta_add_other_case_for_his(array, key):
  index = 0
  count = len(array[key])
  if count == 0:
    return None
  while index < count:
    if key in array[key][index]:
      array[key].append(array[key][index].replace(key, ""))
    index+=1
  return array[key]

def delta_add_other_case_for_others(array, target):
  for key in list(array):
    if key != target:
      index = 0
      count = len(array[key])
      while index < count:
        if target in array[key][index]:
          array[key].append(array[key][index].replace(target, ""))
        index+=1
  return array

def move_terminals_to_new_grammers(array):
  # print("Result until this step:", array)
  for key in list(array):
    # print("\n\n= checking new key:", key)
    index = 0
    count = len(array[key])
    # print("Count of", key,"grammer is",count)
    while index < count:
      value=array[key][index]
      length=len(value)
      # print("\n---- parsing", value)
      # print("Value as", array[key])
      i=0
      while i < length:
        # print("* Value as", array[key])
        if str(value[i]).islower():
          if value[i] not in list(moves):
            name=new_name_for_grammer(array)
            moves[value[i]]=name
            # print("Create", name,"statement for",value[i],"terminal char!",)
            array[name]=[]
            array[name].append(value[i])
          else:
            name=moves[value[i]]
          # print("found", value[i], "in", array[key][index], "will rename to", name)
          array[key][index]=array[key][index].replace(value[i], name)
          # print(array[key])
        # print(value[i])
        i+=1
      index+=1
  return array

def replace_grammer_statement_names(array, key, char):
  print("Found big character(s)", char, "in", key, "statement")
  print("Check move tables:", moves)
  # print(moves.values())
  if char not in list(moves.values()):
    print("Error: find a non-terminal upper-case character, we cannot support one statement with one Upper-case non-terminalestic!")
    sys.exit(-1)
  return array

def formatter_grammers(array):
  for key in list(array):
    index = 0
    count = len(array[key])
    while index < count:
      # if count == 1:
      # elif count >= 2:
      length=len(array[key][index])
      if length == 1:
        if not array[key][index][0].islower():
          array=replace_grammer_statement_names(array, key, array[key][index])
      elif length > 2:
        # print("Found a non-standard grammer:", array[key][index])
        values=array[key][index][1:]
        name=new_name_for_grammer(array)
        # print("Create", name,"statement for", values)
        array[name]=[]
        array[name].append(values)
        array[key][index]=array[key][index].replace(values, name)
      index+=1
  return array

