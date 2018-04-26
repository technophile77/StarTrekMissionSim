#!/usr/bin/env python

import json

from pprint import pprint
from collections import defaultdict
from copy import deepcopy
import missions

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
    #print(json.dumps(skills_by_character,indent=4))
    for skill in skills_by_character:
        pprint(skill)
    #for key in skills_by_character.keys():
    #    pprint("---" + key + "---")
    #    pprint(skills_by_character[key])
    character_by_skills = get_character_by_skills(skill_list,character_data)
    #print(json.dumps(character_by_skills['sarek'],indent=4))
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
                                        slot_skill=find_slot_skill(current_mission,current_slot,mission_data)
                                        new_character=find_available_character_with_skill(slot_skill,skills_by_character,character_assignments)
                                        character_assignments_test=deepcopy(character_assignments)
                                        character_assignments_test[mission['name']][skill]=character
                                        character_assignments_test[current_mission][current_slot]=new_character
                                        test_score=eval_mission_assignments(character_assignments_test,mission_data,character_data)
                                        if test_score > current_score:
                                            pprint("replacing " + character_assignments[current_mission][current_slot] + "(" + str(current_value) + ") with " + new_character + " in mission:" + current_mission + " slot: " + current_slot + "(" + slot_skill + ")")
                                            pprint("replacing " + character_assignments[mission['name']][skill] + "(" + str(current_value) + ") with " + character + "(" + str(skill_value) + ") in mission: " + mission['name'] + " slot: " + skill)
                                            character_assignments[mission['name']][skill]=character
                                            character_assignments[current_mission][current_slot]=new_character
                                            pprint("New score: " + str(test_score) + ", old score:" + str(current_score))


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
        if find_mission.lower() == mission['name'].lower():
            return mission[find_slot]

def find_available_character_with_skill(skill,skills_by_character,character_assignments):
    for character,skill_value in skills_by_character[skill]:
        if is_character_available(character,character_assignments):
            return character
    raise ValueError('character not available with skill: ' + skill)


def is_character_available(character,character_assignments):
    for mission in character_assignments.keys():
        for slot in character_assignments[mission].keys():
            #if(character.lower() == "sarek"):
            #    print("mission: "+mission+" slot: "+slot+" character: '"+character_assignments[mission][slot].lower()+"'")
            if character.lower() == character_assignments[mission][slot].lower():
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
        #pprint(skill_list)
        for skill in skill_list:
            #pprint(skill)
            skill_num=get_character_skill(skill,character)
            if skill_num > 0:
                character_by_skills[character['name']].append((skill,skill_num))
                #pprint(character_by_skills[character['name']])
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
            if skill_words[0] in character.keys():
                skill_num=skill_num + (character[skill_words[0]]*3)
            if skill_words[2] in character.keys():
                skill_num=skill_num + character[skill_words[2]]
            return skill_num*character['bonus']/4
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
            if key == mission['name']:
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
            if key == mission['name']:
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
            for mission_instance in [ item for item in mission_data['missions'] if mission == item['name'] ]:
                skill=mission_instance[slot]
                pprint(skill)
                #pprint(character_by_skills[character])
                # now we know which skill(s) this slot requires
                for skill2, value in [ item2 for item2 in character_by_skills[character] if skill in item2 ]:
                    skill_value=value
                    pprint(value)
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

#this will run the search including frozen characters
#assignments=assign_characters_to_missions("underground movement","fire with fire","connecting the dots","disarmament", mission_data, character_data)
#assignments=assign_characters_to_missions("influence commander","configure mind-sifter","support alliance ally","summon mercenaries", mission_data, character_data)
#assignments=assign_characters_to_missions("treat hirogen hunter","repair comm relay","revise holoprogram","negotiate hunting rights", mission_data, unfrozen_character_data)
#assignments=assign_characters_to_missions("co-opt scientists","raid cold stations","colonize new world","steal eugenics research", mission_data, character_data)
#assignments=assign_characters_to_missions("expose conspiracy","steal starfleet technology","intimidate colony","test officer loyalty", mission_data, character_data)
#assignments=assign_characters_to_missions("support alliance ally","influence commander","summon mercenaries","configure mind-sifter", mission_data, character_data)
#assignments=assign_characters_to_missions("essential cargo","deadlock","shortcuts","still holding on", mission_data, unfrozen_character_data)
#assignments=assign_characters_to_missions("resettle refugees","evaluate sentient ai","hot dog","investigate corruption", mission_data, unfrozen_character_data)
#assignments=assign_characters_to_missions("temporal agent daniels","uploading history","the temporal observatory","mccarthy's blacklist", mission_data, character_data)
#assignments=assign_characters_to_missions("evaluate section 31 base","direct conspiracy","collect terran empire data","evade starfleet agents", mission_data, unfrozen_character_data)
#assignments=assign_characters_to_missions("capture section 31 chief","aid terra prime rallies","intimidate colony","question section 31 spies", mission_data, unfrozen_character_data)
#missions=["rabid dogs","hunting for science","almost real","dueling for science"]
#missions=["third eye","hunting for science","neither snow nor rain","dueling for science"]
#missions=["shock collars","third eye","dueling for science","rabid dogs"]
#missions=["control without fear","self-destruct sequence","neither snow nor rain","almost real"]
#missions=["neither snow nor rain","self-destruct sequence","third eye","rabid dogs"]
#missions=["calm under pressure","self-destruct sequence","third eye","hunting for science"]
#missions=["self-destruct sequence","calm under pressure","neither snow nor rain","almost real"]
#missions=["third eye","no hunting in captivity","hunting for science","almost real"]
#missions=["no hunting in captivity","loners by nature","creature or sentient?","zoology major"]
#missions=["always watching","creature or sentient?","herding cats","the ultimate prize"]
#missions=["humane society","donated by","the comforts of home","creature or sentient?"]
#missions=["loners by nature","the comforts of home","the ultimate prize","herding cats"]
#missions=["donated by","herding cats","the ultimate prize","creature or sentient?"]
#missions=["the ultimate prize","always watching","the comforts of home","humane society"]
#missions=["calm under pressure","hunting for science","humane society","third eye"]
#missions=["control without fear","hunting for science","creature or sentient?","the ultimate prize"]
#missions=["collect terran empire data","direct conspiracy","arrest rally leaders","sisko's self approval"]
#missions=["evade starfleet agents","test agent loyalty","terran empire deep cover","take terran empire devices"]
#missions=["useless information","running on empty","homecoming","dissention in the ranks"]
#missions=["it takes one","repercussions","the tantalus solution","methods and madness"]
#missions=["coming to an understanding","it takes one","repercussions","what's next?"]
#missions=["coming to an understanding","it takes one","what's next?","terror at cold station 12"]
#missions=["repercussions","it takes one","what's next?","burying the hatchet"]
#missions=["it takes one","what's next?","terror at cold station 12","coming to an understanding"]
#missions=["terror at cold station 12","burying the hatchet","what's next?","repercussions"]
#missions=["repercussions","coming to an understanding","it takes one","what's next?"]
#missions=["terror at cold station 12","it takes one","repercussions","coming to an understanding"]
#missions=["terror at cold station 12","coming to an understanding","it takes one","burying the hatchet"]
#missions=["repercussions","burying the hatchet","what's next?","it takes one"]
#missions=["repercussions","it takes one","coming to an understanding","terror at cold station 12"]
#missions=["terror at cold station 12","it takes one","burying the hatchet","what's next?"]
#missions=["breaking chains","the falcon's cry","plague doctors","firewall"]
#missions=["silent listeners","keep your friends close","firewall","you have the floor"]
#missions=["silent listeners","keep your friends close","plague doctors","a vow of inaction"]
#missions=["firewall","a vow of inaction","the falcon's cry","the father of us all"]
#missions=["i spy","silent listeners","you have the floor","the father of us all"]
#missions=["a vow of inaction","the father of us all","keep your friends close","breaking chains"]
#missions=["i spy","firewall","a vow of inaction","silent listeners"]
#missions=["breaking bread","one hand knows not","the magnificent keevan","long live weyoun"]
#missions=["eye for an eye","top secret","the magnificent keevan","one hand knows not"]
#missions=["long live weyoun","silithium signals","top secret","one hand knows not"]
#missions=["top secret","one hand knows not","the missing agent","eye for an eye"]
#missions=["eye for an eye","the missing agent","one hand knows not","silithium signals"]
#missions=["top secret","the missing agent","breaking bread","one hand knows not"]
#missions=["eye for an eye","a changeling voice","breaking bread","top secret"]
#missions=["coded messages","eye for an eye","silithium signals","long live weyoun"]
#missions=["coded messages","breaking bread","top secret","long live weyoun"]
#missions=["silithium signals","the missing agent","coded messages","the magnificent keevan"]
#missions=["a changeling voice","eye for an eye","breaking bread","the magnificent keevan"]
#missions=["manufactured triumph","peanuts and crackerjacks","most consecutive hits","the ferengi's new clothes"]
#missions=["there's no killing in baseball","merchandising potential","learning from the best","team selection"]
#missions=["there's no killing in baseball","merchandising potential","learning from the best","short stop"]
#missions=["manufactured triumph","team selection","up to bat","batting cages"]
#missions=["a league of her own","most consecutive hits","peanuts and crackerjacks","the ferengi's new clothes"]
#missions=["batting cages","team selection","most consecutive hits","up to bat"]
#missions=["short stop","up to bat","batting cages","merchandising potential"]
#missions=["merchandising potential","up to bat","learning from the best","most consecutive hits"]
#missions=["team selection","up to bat","a league of her own","short stop"]
#missions=["let my subjects go","holographic interference","going somewhere?","a spoonful of sugar"]
#missions=["working together","a spoonful of sugar","what lies beneath","going somewhere?"]
#missions=["going somewhere?","working together","let my subjects go","a spoonful of sugar"]
#missions=["holographic interference","let my subjects go","working together","what lies beneath"]
#missions=["going somewhere?","let my subjects go","what lies beneath","working together"]
#missions=["a spoonful of sugar","what lies beneath","let my subjects go","going somewhere?"]
#missions=["holographic interference","let my subjects go","going somewhere?","what lies beneath"]
#missions=["let my subjects go","what lies beneath","going somewhere?","a spoonful of sugar"]
#missions=["going somewhere?","working together","holographic interference","what lies beneath"]
#missions=["truth behind the legend","blueprints","a logical course","roads once traveled"]
#missions=["the weight of memory","vessels","old wounds","roads once traveled"]
#missions=["vessels","truth behind the legend","the needs of the many","calm within the storm"]
#missions=["roads once traveled","the weight of memory","truth behind the legend","philosophical differences"]
#missions=["roads once traveled","the weight of memory","truth behind the legend","philosophical differences"]
#missions=["calm within the storm","roads once traveled","the weight of memory","philosophical differences"]
#missions=["vessels","the needs of the many","old wounds","the weight of memory"]
#missions=["out of synch","vessels","the unchained mind","truth behind the legend"]
#missions=["philosophical differences","out of synch","the weight of memory","calm within the storm"]
#missions=["philosophical differences","calm within the storm","blueprints","the unchained mind"]
#missions=["the weight of memory","roads once traveled","out of synch","old wounds"]
#missions=["truth behind the legend","old wounds","a logical course","vessels"]
#missions=["the unchained mind","old wounds","the weight of memory","out of synch"]
#missions=["calm within the storm","the needs of the many","out of synch","truth behind the legend"]
#missions=["the needs of the many","vessels","philosophical differences","calm within the storm"]
#missions=["vessels","out of synch","roads once traveled","old wounds"]
#missions=["roads once traveled","vessels","calm within the storm","blueprints"]
#missions=["out of synch","calm within the storm","the unchained mind","old wounds"]
#missions=["truth behind the legend","blueprints","out of synch","roads once traveled"]
#missions=["the core of deception","waves beneath the cloak","the neutral zone","a delicate situation"]
#missions=["the neutral zone","the core of deception","aiding the enemy","waves beneath the cloak"]
#missions=["the neutral zone","the core of deception","waves beneath the cloak","adjusting the emitters"]
#missions=["adjusting the emitters","a bit of diplomacy","aiding the enemy","a delicate situation"]
#missions=["by force, if necessary","proper planning","waves beneath the cloak","a delicate situation"]
#missions=["a delicate situation","aiding an enemy","waves beneath the cloak","a bit of diplomacy"]
#missions=["a delicate situation","adjusting the emitters","a bit of diplomacy","waves beneath the cloak"]
#missions=["the element of surprise","adjusting the emitters","waves beneath the cloak","aiding an enemy"]
#missions=["waves beneath the cloak","the neutral zone","adjusting the emitters","aiding an enemy"]
#missions=["disarm first","proper planning","aiding an enemy","the core of deception"]
#missions=["aiding an enemy","footing the bill","disarm first","by force, if necessary"]
#missions=["the neutral zone","disarm first","the core of deception","adjusting the emitters"]
#missions=["adjusting the emitters","the core of deception","the element of surprise","aiding an enemy"]
#missions=["the element of surprise","the neutral zone","aiding an enemy","disarm first"]
#missions=["a bit of diplomacy","waves beneath the cloak","proper planning","the core of deception"]
#missions=["by force, if necessary","the element of surprise","a delicate situation","a bit of diplomacy"]
#missions=["footing the bill","disarm first","a delicate situation","waves beneath the cloak"]
#missions=["adjusting the emitters","disarm first","footing the bill","the neutral zone"]
#missions=["footing the bill","aiding an enemy","by force, if necessary","the core of deception"]
#missions=["they can't change","probing the mind","countermovement","quid pro quo"]
#missions=["hear no evil","they can't change","probing the mind","quid pro quo"]
missions=["those who are left","quid pro quo","hear no evil","probing the mind"]
assignments=assign_characters_to_missions(missions[0],missions[1],missions[2],missions[3], mission_data, unfrozen_character_data)

assignments2=assign_characters_to_missions(missions[0],missions[1],missions[2],missions[3], mission_data, character_data)

#assignments3=assign_characters_to_voyage("science","security",character_data)

#this will run the search excluding frozen characters
#assignments=assign_characters_to_missions("", "escort founder", "verify founder numbers", "vorta experimentation", mission_data, unfrozen_character_data)
#pprint(assignments)

score=eval_mission_assignments(assignments, mission_data, character_data)

pprint("Total score: " + str(score))
for mission in assignments.keys():
    pprint("Mission: " + mission)
    pprint(assignments[mission])

score2=eval_mission_assignments(assignments2, mission_data, character_data)

pprint("Total score: " + str(score2))
for mission in assignments2.keys():
    pprint("Mission: " + mission)
    pprint(assignments2[mission])
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
