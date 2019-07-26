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

def importLogos():
    for i in range(1,22):
        image_name = "Team{}.Logo1".format(i)
        file_name = image_name + ".png"
        bpy.ops.import_image.to_plane(files=[{"name":file_name, "name":file_name}], directory="Users/hyungsoobae/Desktop/K-League/image/")
        models[image_name].location= (0,position1[i-1],1)
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.translate(value=(0,0,0.5), constraint_axis=(False,False,True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.editmode_toggle()


models = bpy.data.objects
scn = bpy.context.scene
data_file_path = "/Users/hyungsoobae/Desktop/K-League/data"
position1 = [0.0, 1.1, 2.2, 3.3000000000000003, 4.4, 5.5, 6.6000000000000005, 7.700000000000001, 8.8, 9.9, 11.0, 12.100000000000001, 13.200000000000001, 14.3, 15.400000000000002, 16.5, 17.6, 18.700000000000003, 19.8, 20.900000000000002, 22.0, 23.1]
tposition1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

outlier = 27

def reset():
    scn.frame_set(0)

    for model in models:
        model.animation_data_clear()
        model.data.animation_data_clear()



    for i in range(1,22):
        #print (models['Team{}'.format(i)].location)
        models['Team{}'.format(i)].location[1] = position1[i-1]
        models['Team{}'.format(i)].scale[2] = 0
        models['Team{}.Point'.format(i)].location[0] = 0.4
        models['Team{}.Point'.format(i)].location[1] = position1[i-1]
        models['Team{}.Point'.format(i)].location[2] = 0.2
        models['Team{}.Point'.format(i)].data.text_counter_props.ifAnimated=True
        models['Team{}.Point'.format(i)].data.text_counter_props.counter = 0

        for j in range(1,6):
            try:
                models['Team{}.Name{}'.format(i,j)].location[1] = position1[i-1]
                models['Team{}.Name{}'.format(i,j)].location[2] = 1.8
                models['Team{}.Name{}'.format(i,j)].rotation_euler[1] = -0.872665
                models['Team{}.Name{}'.format(i,j)].data.size = 0.45
            except:
                pass

        for j in range(1,8):
            try:
                models['Team{}.Logo{}'.format(i, j)].location[1] = position1[i-1]
                models['Team{}.Logo{}'.format(i, j)].location[2] = 0.8
            except:
                pass




def get_current_teams(frame=0):
    result = []
    scn.frame_set(frame)
    for model in models:
        if 'Team' in model.name and '.' not in model.name:
            if (model.location[1]) < outlier:
                result.append(model)
    result.sort(key=lambda x : x.location[1])
    result = list(map(lambda x: x.name, result))
    return result

def setNameLocation(ffrom, frame, teamName, value):
    for i in range(1,6):
        try:
            scn.frame_set(ffrom)
            models['{}.Name{}'.format(teamName,i)].keyframe_insert(data_path='location')

            scn.frame_set(ffrom+frame)
            models['{}.Name{}'.format(teamName, i)].location[1] = value
            models['{}.Name{}'.format(teamName, i)].location[2] = models[teamName].scale[2] * 2 + 1.8
            models['{}.Name{}'.format(teamName, i)].keyframe_insert(data_path='location')
        except:
            pass

def setLogoLocation(ffrom, frame, teamName, value):
    for i in range(1,8):
        try:
            scn.frame_set(ffrom)
            models['{}.Logo{}'.format(teamName,i)].keyframe_insert(data_path='location')

            scn.frame_set(ffrom+frame)
            models['{}.Logo{}'.format(teamName, i)].location[1] = value
            models['{}.Logo{}'.format(teamName, i)].location[2] = models[teamName].scale[2] * 2 + 0.8
            models['{}.Logo{}'.format(teamName, i)].keyframe_insert(data_path='location')
        except:
            pass

def setPointLocation(ffrom, frame, teamName, value, point=None):
        scn.frame_set(ffrom)
        models['{}.Point'.format(teamName)].keyframe_insert(data_path='location')

        if point is not None:
            models['{}.Point'.format(teamName)].data.keyframe_insert(data_path='text_counter_props.counter')


        scn.frame_set(ffrom+frame)
        models['{}.Point'.format(teamName)].location[1] = value
        if models[teamName].scale[2] > 0:
            models['{}.Point'.format(teamName)].location[2] = models[teamName].scale[2] * 2 + 0.2
        else:
            models['{}.Point'.format(teamName)].location[2] = 0.2

        if point is not None:
            models['{}.Point'.format(teamName)].data.text_counter_props.counter = point
            models['{}.Point'.format(teamName)].data.keyframe_insert(data_path='text_counter_props.counter')


        models['{}.Point'.format(teamName)].keyframe_insert(data_path='location')

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
    print (current_teams)

    #Remove all non participitating teams from the table
    np_teams = set(current_teams) - new_teams_set

    for team in np_teams:
        #print (team)
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')
        models[team].keyframe_insert(data_path='scale')

        scn.frame_set(ffrom+frame)
        models[team].location[1] = outlier
        models[team].scale[2] = 0
        models[team].keyframe_insert(data_path='location')
        models[team].keyframe_insert(data_path='scale')


        setNameLocation(ffrom, frame, team, outlier)
        setLogoLocation(ffrom, frame, team, outlier)
        setPointLocation(ffrom, frame, team, outlier, 0)

    #Move the old teams in order
    current_teams = list(filter(lambda x: x not in np_teams, current_teams))
    current_number = len(current_teams)
    for i,team in enumerate(current_teams):
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team].location[1] = position1[i]
        models[team].keyframe_insert(data_path='location')

        setNameLocation(ffrom, frame, team, position1[i])
        setLogoLocation(ffrom, frame, team, position1[i])
        setPointLocation(ffrom, frame, team, position1[i])

    #Add new teams
    new_teams_set = new_teams_set - set(current_teams)
    for i,team in enumerate(new_teams_set):
        scn.frame_set(ffrom)
        models[team].keyframe_insert(data_path='location')

        scn.frame_set(ffrom+frame)
        models[team].location[1] = position1[current_number+i]
        models[team].keyframe_insert(data_path='location')

        setNameLocation(ffrom, frame, team, position1[current_number+i])
        setLogoLocation(ffrom, frame, team, position1[current_number+i])
        setPointLocation(ffrom, frame, team, position1[current_number+i])

def league_type_1(year, ffrom, frame, scale=10):
    new_teams = []
    new_teams_set = set()

    fp = data_file_path + "/" + year + ".csv"
    with open(fp, 'r', encoding="utf-8") as csvfile:
        rdr = csv.reader(csvfile)
        for i,v in enumerate(rdr):
            new_teams.append((i,v[2],int(v[1])))
            new_teams_set.add(v[2])
    #print (new_teams)

    for team in new_teams:
        scn.frame_set(ffrom)
        models[team[1]].keyframe_insert(data_path='location')
        models[team[1]].keyframe_insert(data_path='scale')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].scale[2] = team[2] / scale
        models[team[1]].keyframe_insert(data_path='location')
        models[team[1]].keyframe_insert(data_path='scale')

        setNameLocation(ffrom, frame, team[1], position1[team[0]])
        setLogoLocation(ffrom, frame, team[1], position1[team[0]])
        setPointLocation(ffrom, frame, team[1], position1[team[0]], team[2])

def league_type_3(year, ffrom, frame, scale):
    league_type_1(year,ffrom,frame, scale)

def league_type_4(year, ffrom, frame, scale):
    league_type_1(year,ffrom,frame, scale)

def post_season(year, ffrom, frame, scale):
    league_type_1(year+'p',ffrom,frame, scale)


def league_type_5(year, ffrom, frame, scale):
    league_type_1(year,ffrom,frame, scale)

def split(year, ffrom, frame, gap=2, scale=10):
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
        models[team[1]].keyframe_insert(data_path='scale')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[team[0]]
        models[team[1]].scale[2] = team[2] / scale
        models[team[1]].keyframe_insert(data_path='location')
        models[team[1]].keyframe_insert(data_path='scale')

        setNameLocation(ffrom, frame, team[1], position1[team[0]])
        setLogoLocation(ffrom, frame, team[1], position1[team[0]])
        setPointLocation(ffrom, frame, team[1], position1[team[0]], team[2])

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
        models[team[1]].keyframe_insert(data_path='scale')

        scn.frame_set(ffrom+frame)
        models[team[1]].location[1] = position1[length-1+gap+team[0]]
        models[team[1]].scale[2] = team[2] / scale
        models[team[1]].keyframe_insert(data_path='location')
        models[team[1]].keyframe_insert(data_path='scale')

        setNameLocation(ffrom, frame, team[1],position1[length-1+gap+team[0]])
        setLogoLocation(ffrom, frame, team[1],position1[length-1+gap+team[0]])
        setPointLocation(ffrom, frame, team[1],position1[length-1+gap+team[0]], team[2])



reset()
transition("1983", 0, 5)
league_type_1("1983", 5, 50, 30)



'''
league_type_3('1999',35,30)
post_season('1999', 70, 30)

transition("2012", 105, 30)
league_type_5("2012", 150, 30)
split("2012", 185,30)



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
