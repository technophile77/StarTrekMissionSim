#!/usr/bin/env python

import json

from pprint import pprint
from collections import defaultdict
from copy import deepcopy


#pprint(mission_data)

#pprint(character_data)

def assign_characters_to_missions(mission_name1, mission_name2, mission_name3, mission_name4, mission_data, character_data):
    mission_list=[]
    for mission in mission_data['missions']:
        #pprint(mission)
        if mission['name'].lower() == mission_name1.lower():
            pprint("mission 1 matched: " + mission['name'])
            mission_list.append(mission)
        if mission['name'].lower() == mission_name2.lower():
            pprint("mission 2 matched: " + mission['name'])
            mission_list.append(mission)
        if mission['name'].lower() == mission_name3.lower():
            pprint("mission 3 matched: " + mission['name'])
            mission_list.append(mission)
        if mission['name'].lower() == mission_name4.lower():
            pprint("mission 4 matched: " + mission['name'])
            mission_list.append(mission)
    mission_list.sort(key = lambda r: len(r))
    #pprint(mission_list)
    character_assignments=defaultdict(dict)
    for mission in mission_list:
        mission_skills={}
        for skill in mission:
            if "slot" in skill:
                mission_skills[skill]=""
        character_assignments[mission['name']]=mission_skills
    #pprint(character_assignments)
    skill_list=[]
    skill_list=get_skill_list(mission_list)
    #pprint(skill_list)
    skills_by_character = get_skills_by_character(skill_list,character_data)
    #pprint(skills_by_character)
    #for key in skills_by_character.keys():
    #    pprint("---" + key + "---")
    #    pprint(skills_by_character[key])
    character_by_skills = get_character_by_skills(skill_list,character_data)
    #pprint(character_by_skills)
    for depth in range(len(skill_list)):
        for mission in mission_list:
            for skill in mission:
                if "slot" in skill:
                    #pprint(mission[skill])
                    #pprint("looking for skill: " + mission[skill])
                    for character,skill_value in skills_by_character[mission[skill]]:
                        # here we are going through the characters that match the skill required for the slot
                        #pprint(character_by_skills[character])
                        if(depth < len(character_by_skills[character])):
                            (skill_n,value_n)=character_by_skills[character][depth]
                            # here we are picking up the depth'th highest skill from the character, sorted highest to lowest
                            #pprint("comparing " + mission[skill] + " " + str(skill_value) + " to " + skill_n + " " + str(value_n))
                            # if the skill we want to use for this slot is higher than or equal to the depth'th skill, then we use it
                            # as we increase depth, we will have the opportunity to use lower rank skills, IF they are higher than
                            # the skill of the character that is currently selected
                            if skill_value >= value_n:
                                character_available=True
                                for mission_check in character_assignments:
                                    #pprint(character_assignments)
                                    #pprint("mission: " + mission_check)
                                    for slot_check in character_assignments[mission_check]:
                                        #pprint (slot_check)
                                        if "slot" in slot_check:
                                            #pprint(character_assignments[mission_check][slot_check])
                                            #pprint("Character: " + character)
                                            if character in character_assignments[mission_check][slot_check]:
                                                character_available=False
                                                #pprint("character: " + character + " already assigned to " + mission_check + " slot " + slot_check)
                                if character_available:
                                    if not character_assignments[mission['name']][skill]:
                                        #pprint(skill)
                                        pprint("initial assignment " + character + " to mission: " + mission['name'] + " slot: " + skill)
                                        character_assignments[mission['name']][skill]=character
                                    else:
                                        #(current_skill,current_value)=[mission[skill]] in character_by_skills[character_assignments[mission['name']][skill]]
                                        #pprint("character: " + character_assignments[mission['name']][skill])
                                        #pprint(character_by_skills[character_assignments[mission['name']][skill]])
                                        #pprint("skill: " + mission[skill])
                                        list=[item for item in character_by_skills[character_assignments[mission['name']][skill]] if mission[skill].lower() in item]
                                        #pprint(list)
                                        (current_skill,current_value)=list[0]
                                        if skill_value > current_value:
                                            pprint("replacing " + character_assignments[mission['name']][skill] + " with " + character + " in mission: " + mission['name'] + " slot: " + skill)
                                            character_assignments[mission['name']][skill]=character
    # at this point we should have all slots filled, if we have enough characters.
    # next we will try moving characters around and pulling in new characters
    for depth in range(len(skill_list)):
        for mission in mission_list:
            for skill in mission:
                if "slot" in skill:
                    #pprint(mission[skill])
                    #pprint("looking for skill: " + mission[skill])
                    for character,skill_value in skills_by_character[mission[skill]]:
                        # here we are going through the characters that match the skill required for the slot
                        #pprint(character_by_skills[character])
                        if(depth < len(character_by_skills[character])):
                            (skill_n,value_n)=character_by_skills[character][depth]
                        else:
                            (skill_n,value_n)=character_by_skills[character][len(character_by_skills[character])-1]
                        # here we are picking up the depth'th highest skill from the character, sorted highest to lowest
                        #pprint("comparing " + mission[skill] + " " + str(skill_value) + " to " + skill_n + " " + str(value_n))
                        # if the skill we want to use for this slot is higher than or equal to the depth'th skill, then we use it
                        # as we increase depth, we will have the opportunity to use lower rank skills, IF they are higher than
                        # the skill of the character that is currently selected
                        if skill_value >= value_n:
                            list=[item for item in character_by_skills[character_assignments[mission['name']][skill]] if mission[skill].lower() in item]
                            #pprint(list)
                            if list:
                                (current_skill,current_value)=list[0]
                                if skill_value > current_value:
                                    #pprint("testing " + character_assignments[mission['name']][skill] + "(" + str(current_value) + ") with " + character + "(" + str(skill_value) + ") in mission: " + mission['name'] + " slot: " + skill)
                                    current_score=eval_mission_assignments(character_assignments,mission_data,character_data)
                                    if is_character_available(character,character_assignments):
                                        pprint("replacing " + character_assignments[mission['name']][skill] + "(" + str(current_value) + ") with " + character + "(" + str(skill_value) + ") in mission: " + mission['name'] + " slot: " + skill)
                                        character_assignments[mission['name']][skill]=character
                                        current_score=eval_mission_assignments(character_assignments,mission_data,character_data)
                                        pprint("New score: " + str(current_score))
                                    else:
                                        (current_mission,current_slot)=where_is_character_assigned(character,character_assignments)
                                        slot_skill=find_slot_skill(mission['name'],skill,mission_data)
                                        new_character=find_available_character_with_skill(slot_skill,skills_by_character,character_assignments)
                                        character_assignments_test=deepcopy(character_assignments)
                                        character_assignments_test[mission['name']][skill]=character
                                        character_assignments_test[current_mission][current_slot]=new_character
                                        test_score=eval_mission_assignments(character_assignments_test,mission_data,character_data)
                                        if test_score > current_score:
                                            pprint("replacing " + character_assignments[mission['name']][skill] + "(" + str(current_value) + ") with " + character + "(" + str(skill_value) + ") in mission: " + mission['name'] + " slot: " + skill)
                                            character_assignments[mission['name']][skill]=character
                                            character_assignments[current_mission][current_slot]=new_character
                                            current_score=eval_mission_assignments(character_assignments,mission_data,character_data)
                                            pprint("New score: " + str(current_score))


    return character_assignments

def validate_characters(character_data):
    for character in character_data['characters']:
        if 'name' in character.keys():
            name=character['name']
        else:
            pprint(character)
            raise ValueError('found a character lacking a name trait')
        if not type(name) in [str,unicode]:
            pprint(name)
            pprint(type(name))
            raise ValueError('found a character with non-string name')
        for key in character.keys():
            if not key in ['name','bonus','frozen','command','diplomacy','security','science','engineering','medicine','frozen']:
                pprint(key)
                raise ValueError('found an unknown key in character: ' + character['name'])
        if 'bonus' in character.keys():
            bonus=character['bonus']
        else:
            raise ValueError('character: ' + name + ' has no bonus value')
        if not isinstance(bonus,int):
            raise ValueError('character: ' + name + ' has a non number or string for bonus')
        traits=[item for item in character.keys() if item in ["command","diplomacy","security","science","engineering","medicine"]]
        if len(traits) < 1:
            raise ValueError('character: ' + character['name'] + ' has no abilities')
        for trait in traits:
            if not isinstance(character[trait],int):
                pprint(character[trait])
                raise ValueError('character: ' + character['name'] + ' has a trait: ' + trait + ' with a non-numeric value')
    for character in character_data['characters']:
        duplicates=[item for item in character_data['characters'] if item['name'] == character['name']]
        if len(duplicates) > 1:
            raise ValueError('found ' + str (len(duplicates)) + ' copies of character: ' + character['name'])
    return 0

def find_slot_skill(find_mission,find_slot,mission_data):
    for mission in mission_data['missions']:
        if find_mission.lower() in mission['name']:
            return mission[find_slot]

def find_available_character_with_skill(skill,skills_by_character,character_assignments):
    for character,skill_value in skills_by_character[skill]:
        if is_character_available(character,character_assignments):
            return character
    raise ValueError('character not available with skill: ' + skill)


def is_character_available(character,character_assignments):
    for mission in character_assignments.keys():
        for slot in character_assignments[mission].keys():
            if character.lower() in character_assignments[mission][slot].lower():
                return False
    return True

def where_is_character_assigned(character,character_assignments):
    for mission in character_assignments.keys():
        for slot in character_assignments[mission].keys():
            if character.lower() in character_assignments[mission][slot].lower():
                return (mission,slot)
    raise ValueError('character not found: ' + character)

def get_skills_by_character(skill_list, character_data):
    skills_by_character = defaultdict(list)
    for skill in skill_list:
        for character in character_data['characters']:
            skill_num=get_character_skill(skill,character)
            if skill_num > 0:
                skills_by_character[skill].append((character['name'],skill_num))
    for skill in skills_by_character:
        skills_by_character[skill].sort(key=lambda r: r[1],reverse=True)
    return skills_by_character


def get_character_by_skills(skill_list, character_data):
    character_by_skills = defaultdict(list)
    for character in character_data['characters']:
        for skill in skill_list:
            skill_num=get_character_skill(skill,character)
            if skill_num > 0:
                character_by_skills[character['name']].append((skill,skill_num))
    for character in character_by_skills:
        character_by_skills[character].sort(key=lambda r: r[1],reverse=True)
    return character_by_skills


def get_skill_list(mission_list):
    skill_list=[]
    for mission in mission_list:
        for slot in mission:
            if "slot" in slot.lower():
                #pprint(mission[slot])
                if mission[slot].lower() not in skill_list:
                    #pprint("appending " + mission[slot].lower())
                    skill_list.append(mission[slot].lower())
    return skill_list

def get_character_skill(skill, character):
    if skill.lower() in ["command","diplomacy","security","engineering","medicine","science"]:
        for thing in character:
            if skill.lower() == thing.lower():
                return character[thing]*character['bonus']
        #pprint("character: " + character['name'] + " has no skill: " + skill)
        return 0
    else:
        skill_words=skill.split()
        if "or" in skill_words:
            skill_num=0
            for thing in character:
                if thing.lower() in skill_words:
                    if character[thing] > skill_num:
                        skill_num=character[thing]
            return skill_num*character['bonus']
        elif "and" in skill_words:
            skill_num=0
            for skill in skill_words:
                if skill in character.keys():
                    skill_num=skill_num + character[skill]
            return skill_num*character['bonus']/2
        else:
            raise ValueError('skill not recognized: ' + skill)
            return 0
    return 0

def eval_mission_assignments(character_assignments, mission_data, character_data):
    total_score=0
    mission_list=[]
    mission_keys=character_assignments.keys()
    #pprint(character_assignments)
    for key in mission_keys:
        for mission in mission_data['missions']:
            if key in mission['name']:
                mission_list.append(mission)
    #pprint(mission_list)
    skill_list=get_skill_list(mission_list)
    #pprint(skill_list)
    skills_by_character = get_skills_by_character(skill_list,character_data)
    character_by_skills = get_character_by_skills(skill_list,character_data)
    #pprint(character_by_skills)
    for mission_element in mission_list:
        mission=mission_element['name']
        mission_value=0
        #pprint(character_assignments[mission])
        for slot in character_assignments[mission]:
            character=character_assignments[mission][slot]
            #pprint(character)
            # now we know which character is assigned to this slot
            for mission_instance in [ item for item in mission_data['missions'] if mission in item['name'] ]:
                skill=mission_instance[slot]
                #pprint(skill)
                #pprint(character_by_skills[character])
                # now we know which skill(s) this slot requires
                for skill2, value in [ item2 for item2 in character_by_skills[character] if skill in item2 ]:
                    skill_value=value
                    #pprint(value)
                    mission_value=mission_value+skill_value
        #pprint("Mission total: " + str(mission_value))
        mission_average=mission_value/(len(mission_element)-1) # we have to adjust for the name element which doesn't count
        #pprint("Mission average: " + str(mission_average))
        total_score=total_score+mission_average
    return total_score


def eval_mission_assignments_debug(character_assignments, mission_data, character_data):
    total_score=0
    mission_list=[]
    mission_keys=character_assignments.keys()
    #pprint(character_assignments)
    for key in mission_keys:
        for mission in mission_data['missions']:
            if key in mission['name']:
                mission_list.append(mission)
    #pprint(mission_list)
    skill_list=get_skill_list(mission_list)
    #pprint(skill_list)
    skills_by_character = get_skills_by_character(skill_list,character_data)
    character_by_skills = get_character_by_skills(skill_list,character_data)
    #pprint(character_by_skills)
    for mission_element in mission_list:
        mission=mission_element['name']
        mission_value=0
        #pprint(character_assignments[mission])
        for slot in character_assignments[mission]:
            character=character_assignments[mission][slot]
            #pprint(character)
            # now we know which character is assigned to this slot
            for mission_instance in [ item for item in mission_data['missions'] if mission in item['name'] ]:
                skill=mission_instance[slot]
                #pprint(skill)
                #pprint(character_by_skills[character])
                # now we know which skill(s) this slot requires
                for skill2, value in [ item2 for item2 in character_by_skills[character] if skill in item2 ]:
                    skill_value=value
                    #pprint(value)
                    mission_value=mission_value+skill_value
        pprint("Mission total: " + str(mission_value))
        mission_average=mission_value/(len(mission_element)-1) # we have to adjust for the name element which doesn't count
        pprint("Mission average: " + str(mission_average))
        total_score=total_score+mission_average
    return total_score

def filter_frozen_characters(character_data):
    character_data_filtered_list=[item for item in character_data['characters'] if not is_frozen(item)]
    character_data_filtered=defaultdict(list)
    character_data_filtered['characters']=character_data_filtered_list
    return character_data_filtered

def is_frozen(character):
    if "frozen" in character.keys():
        if character['frozen']:
            return True
    return False
#def display_assignments(character_assignments,mission_data,character_data):


with open('missions.json') as mission_file:
  mission_data = json.load(mission_file)

with open('characters.json') as character_file:
    character_data = json.load(character_file)

validate_characters(character_data)

unfrozen_character_data=filter_frozen_characters(character_data)

assignments=assign_characters_to_missions("mercy mission", "escort founder", "sector reconnaissance", "vorta experimentation", mission_data, unfrozen_character_data)
for mission in assignments.keys():
    pprint("Mission: " + mission)
    pprint(assignments[mission])
#pprint(assignments)

score=eval_mission_assignments(assignments, mission_data, character_data)

pprint("Total score: " + str(score))

#test=is_character_available("captain q",assignments)

#if test:
#    pprint("captain q is not assigned")
#else:
#    pprint("captain q is assigned")

#test2=is_character_available("automated unit 3947",assignments)

#if test2:
#    pprint("APU 3947 is not assigned")
#else:
#    pprint("APU 3947 is assigned")

#skill_num=get_character_skill("diplomacy",character_data['characters'][0])
#pprint(character_data['characters'][0]['name'] + " skill diplomacy is " + str(skill_num))
