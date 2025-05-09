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
  if len(parts) != 2:
    print(f"Error parsing line: {line}. Format should be 'A -> B'")
    continue
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
    return array[key]
  while index < count:
    if key in array[key][index]:
      new_prod = array[key][index].replace(key, "")
      if new_prod and new_prod not in array[key]:
        array[key].append(new_prod)
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
  # If the character is a non-terminal (already defined)
  if char in array:
    return array
  
  # If it's not in moves values, it's a new non-terminal we need to handle
  if char not in list(moves.values()):
    print(f"Warning: Found non-terminal {char} in {key} statement that isn't from a terminal conversion")
    # Let's not exit since this is valid for existing non-terminals
  
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

# Remove epsilon productions
def remove_epsilon_productions(array):
  has_epsilon = {}
  # Find all non-terminals that derive epsilon
  for key in list(array):
    if "$" in array[key]:
      has_epsilon[key] = True
      array[key].remove("$")
  
  # Add new productions
  for key in list(array):
    new_productions = []
    for production in array[key]:
      for nullable in has_epsilon:
        if nullable in production:
          # Add new production without the nullable symbol
          new_prod = production.replace(nullable, "", 1)
          if new_prod and new_prod not in array[key] and new_prod not in new_productions:
            new_productions.append(new_prod)
    
    array[key].extend(new_productions)
  
  return array

# Remove unit productions (A -> B)
def remove_unit_productions(array):
  changed = True
  while changed:
    changed = False
    for key in list(array):
      unit_prods = []
      for i, prod in enumerate(array[key]):
        if len(prod) == 1 and prod.isupper():
          unit_prods.append((i, prod))
      
      # Process unit productions
      for i, unit in sorted(unit_prods, reverse=True):
        array[key].pop(i)
        if unit in array:
          for replacement in array[unit]:
            if replacement not in array[key]:
              array[key].append(replacement)
              changed = True
  
  return array

# Apply the CFG to CNF conversion
def convert_to_cnf(array):
  # Step 1: Remove epsilon productions
  array = remove_epsilon_productions(array)
  
  # Step 2: Remove unit productions
  array = remove_unit_productions(array)
  
  # Step 3: Move terminals to new grammars
  array = move_terminals_to_new_grammers(array)
  
  # Step 4: Format grammers (split productions with more than 2 non-terminals)
  array = formatter_grammers(array)
  
  return array

# Print the grammar in a nice format
def print_grammar(array):
  print("\nResulting CNF Grammar:")
  for key in sorted(array.keys()):
    productions = " | ".join(array[key]) if array[key] else "$"
    print(f"{key} -> {productions}")

# Process the input grammar
print("\nProcessing grammar...")
rules = convert_to_cnf(rules)
print_grammar(rules)
print("\nConversion completed successfully.")

