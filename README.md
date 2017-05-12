# StarTrekMissionSim

This is a pretty simple tool that will optimize your character assignment to shuttle missions to get the highest overall average skill across 1-4 shuttles. I made this tool because I was sure that I wasn't doing the best possible job, and with testing I have validated that this tool regularly beats my assignments by 5-10%.

How it works:
There are two key data files that you need to populate in before you run the tool.
characters.json - should have a list of characters you have available, if you want to include characters that you have frozen, then it may select these characters, so you will have to unfreeze them when needed. The bonus field is there so that during events you can indicate which multiplier (for featured crew) to use for that particular character. It's a multiplier of 3 for specific characters featured, and 2 for different versions of the character, or for factions included (vulcans, klingon, etc.). Don't forget to change these back to 1 after the event is over, or you'll probably start failing lots of missions.

missions.json - I have only set up some event missions, and these vary by event, so you will probably want to edit these each time. I plan to include the regular faction missions (because these do not change) in the next release, or if someone wants to help contribute I please send a pull request with this data file.

The script fill.py, you will need python installed with the following modules available: json, pprint, defaultdict, and deepcopy.

The magic really happens in the function assign_characters_to_missions. When you call this function you pass the names of the missions you want to send, it accepts up to 4 missions, and will do less if you leave an empty string in the mission names that you don't want to use.

This will return a set of character assignments which should then get printed by the code below that call, and that's pretty much how to use it.

I don't want to get too much into how it works, but it's definately not the most efficient algorithm, but the completion time is reasonable for me, so unless there is some problem with it, I probably won't tweak how it works. The overall goal of the algorithm is to get the highest possible sum of average skills across the missions you assign it. Mission success is based off average skill level in a mission, so whether a mission requires 2 characters or 5 characters, the average is what counts. Aiming for the highest sum of averages seems like the right approach, but it could also be argued that you don't want to let one mission fall too low just to get a really high score in another mission, so I may introduce some other options for optimization types (especially if there is a request for it) in future.

I would highly encourage that you check your results, no guarantee that this will give the best results. I'll be happy to fix relevant bugs, etc. As far as making this a more user friendly tool, I'm not especially interested in that, but I would be happy to work with someone if they want to include this as a backend to something more user friendly.


TODO LIST:
- [ ] add remaining faction missions to missions.json
- [ ] add command line options:missions and unfreeze
