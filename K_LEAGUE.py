import bpy
import csv
import os
from bpy import context
import builtins as __builtin__

def console_print(*args, **kwargs):
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {}
            c['area'] = a
            c['space_data'] = a.spaces.active
            c['region'] = a.regions[-1]
            c['window'] = context.window
            c['screen'] = context.screen
            s = " ".join([str(arg) for arg in args])
            for line in s.split("\n"):
                bpy.ops.console.scrollback_append(c, text=line)


def print(*args, **kwargs):
    """Console print() function."""

    console_print(*args, **kwargs) # to py consoles
    __builtin__.print(*args, **kwargs) # to system console


models = bpy.data.objects
scn = bpy.context.scene
data_file_path = "/Users/hyungsoobae/Desktop/K-League/data"
position1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
outlier = 20

def reset():
    for model in models:
        model.animation_data_clear()
        model.data.animation_data_clear()

    scn.frame_set(0)

    for i in range(1,22):
        #print (models['Team{}'.format(i)].location)
        models['Team{}'.format(i)].location[1] = position1[i-1]
        models['Team{}.Name1'.format(i)].location[1] = position1[i-1]
        models['Team{}.Name1'.format(i)].data.size = 0.7


    for i in range(1,22):
        models['Team{}'.format(i)].scale[2] = 0.4



def get_current_teams(frame=0):
    result = []
    scn.frame_set(frame)
    for model in models:
        if 'Team' in model.name:
            if (model.location[1]) < 20:
                result.append(model)
    result.sort(key=lambda x : x.location[1])
    result = list(map(lambda x: x.name, result))
    return result


def transition(year, ffrom, frame):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + ".csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    current_teams = get_current_teams(ffrom)

    #Remove all non participitating teams from the table
    np_teams = set(current_teams) - new_teams_set

    for team in np_teams:
        #print (team)
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')
        scn.frame_set(ffrom+frame)
        models[team].location[1] = outlier
        models[team].keyframe_insert(data_path='location')

    #Move the old teams in order
    current_teams = list(filter(lambda x: x not in np_teams, current_teams))
    current_number = len(current_teams)
    for i,team in enumerate(current_teams):
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')
        models['{}.Name1'.format(team)].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team].location[1] = position1[i]
        models['{}.Name1'.format(team)].location[1] = position1[i]
        models['{}.Name1'.format(team)].keyframe_insert(data_path='location')
        models[team].keyframe_insert(data_path='location')

    #Add new teams
    new_teams_set = new_teams_set - set(current_teams)
    for i,team in enumerate(new_teams_set):
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')
        models['{}.Name1'.format(team)].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team].location[1] = position1[current_number+i]
        models['{}.Name1'.format(team)].location[1] = position1[current_number+i]
        models[team].keyframe_insert(data_path='location')
        models['{}.Name1'.format(team)].keyframe_insert(data_path='location')

def league_type_1(year, ffrom, frame):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + ".csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])
    print (new_teams)

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].keyframe_insert(data_path='location')

def league_type_3(year, ffrom, frame):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + ".csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].keyframe_insert(data_path='location')


def post_season(year, ffrom, frame):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + "p.csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].keyframe_insert(data_path='location')


def league_type_5(year, ffrom, frame):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + ".csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].keyframe_insert(data_path='location')

def split(year, ffrom, frame, gap=2):
    new_teams = []
    new_teams_set = set()

    #GROUP A
    fp = data_file_path + "/" + year + "a.csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    length = len(new_teams)

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].keyframe_insert(data_path='location')

    #GROUP B
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + "b.csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])

    length = len(new_teams)

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[length-1+gap+team[0]]
        models[team[1]].keyframe_insert(data_path='location')



reset()
#transition("1999", 0, 30)
#transition("2012", 105, 30)

'''
transition("1999", 0, 30)
transition("1999", 0, 30)
league_type_1('1999',35,30)
post_season('1999', 70, 30)
transition("2012", 105, 30)
league_type_5("2012", 150, 30)
split("2012", 185,30)

transition("1992", 220, 30)
league_type_1('1992',255,30)


transition("1983", 0, 30)
transition("1992", 35, 30)
league_type_1('1992',75,30)
transition("1999", 70, 30)
transition("2007", 105, 30)
'''
