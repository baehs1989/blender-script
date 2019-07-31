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
        if 'Year' in model.name:
            continue
        if 'Team' in model.name and 'Name' in model.name:
            index = []
            for i,action in enumerate(model.animation_data.action.fcurves):
                if action.data_path == 'location':
                    index.append(i)
            for i in range(len(index)):
                print (index)
                model.animation_data.action.fcurves.remove(model.animation_data.action.fcurves[index[i]])
                index = list(map(lambda x: x-1, index))
                print (index)
            continue

        model.animation_data_clear()
        model.data.animation_data_clear()

    for i in range(1,23):
        #print (models['Team{}'.format(i)].location)
        models['Team{}'.format(i)].location[1] = position1[i-1]
        models['Team{}'.format(i)].scale[2] = 0
        models['Team{}.Point'.format(i)].location[0] = 0.4
        models['Team{}.Point'.format(i)].location[1] = position1[i-1]
        models['Team{}.Point'.format(i)].location[2] = 0.4
        models['Team{}.Point'.format(i)].data.text_counter_props.ifAnimated=True
        models['Team{}.Point'.format(i)].data.text_counter_props.counter = 0

        for j in range(1,6):
            try:
                models['Team{}.Name{}'.format(i,j)].location[1] = position1[i-1]
                models['Team{}.Name{}'.format(i,j)].location[2] = 2.1
                models['Team{}.Name{}'.format(i,j)].rotation_euler[1] = -0.872665
                models['Team{}.Name{}'.format(i,j)].data.size = 0.3
            except:
                pass

        for j in range(1,8):
            try:
                models['Team{}.Logo{}'.format(i, j)].location[1] = position1[i-1]
                models['Team{}.Logo{}'.format(i, j)].location[2] = 1.0
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
            models['{}.Name{}'.format(teamName, i)].location[2] = models[teamName].scale[2] * 2 + 2.1
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
            models['{}.Logo{}'.format(teamName, i)].location[2] = models[teamName].scale[2] * 2 + 1.0
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
            models['{}.Point'.format(teamName)].location[2] = models[teamName].scale[2] * 2 + 0.4
        else:
            models['{}.Point'.format(teamName)].location[2] = 0.4

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

'''
reset()

transition("1983", 0, 5)
league_type_1("1983", 5, 50, 40)

transition("1984a", 105, 15)
league_type_1("1984a", 120, 50, 40)
league_type_1("1984b", 195, 50, 40)
league_type_1("1984c", 270, 25, 40)

transition("1985", 345, 15)
league_type_1("1985", 360, 50, 40)

transition("1986a", 460, 15)
league_type_1("1986a", 475, 50, 40)
league_type_1("1986b", 550, 50, 40)
league_type_1("1986c", 625, 25, 40)

transition("1987", 700, 15)
league_type_1("1987", 715, 50, 40)

transition("1988", 815, 15)
league_type_1("1988", 830, 50, 40)

transition("1989", 930, 15)
league_type_1("1989", 945, 50, 40)

transition("1990", 1045, 15)
league_type_1("1990", 1060, 50, 40)

transition("1991", 1160, 15)
league_type_1("1991", 1175, 50, 40)

transition("1992", 1275, 15)
league_type_1("1992", 1290, 50, 40)

transition("1993", 1390, 15)
league_type_1("1993", 1405, 50, 40)

transition("1994", 1505, 15)
league_type_1("1994", 1520, 50, 40)

transition("1995a", 1620, 15)
league_type_1("1995a", 1635, 50, 40)
league_type_1("1995b", 1710, 50, 40)
league_type_1("1995c", 1785, 25, 40)

transition("1996a", 1860, 15)
league_type_1("1996a", 1875, 50, 40)
league_type_1("1996b", 1950, 50, 40)
league_type_1("1996c", 2025, 25, 40)

transition("1997", 2100, 15)
league_type_1("1997", 2115, 50, 40)

transition("1998", 2215, 15)
league_type_1("1998", 2230, 50, 40)
post_season("1998", 2305, 25, 40)

transition("1999", 2380, 15)
league_type_1("1999", 2395, 50, 40)
post_season("1999", 2470, 25, 40)

transition("2000", 2545, 15)
league_type_1("2000", 2560, 50, 40)
post_season("2000", 2635, 25, 40)

transition("2001", 2710, 15)
league_type_1("2001", 2725, 50, 40)

transition("2002", 2825, 15)
league_type_1("2002", 2840, 50, 40)

transition("2003", 2940, 15)
league_type_1("2003", 2955, 50, 40)

transition("2004a", 3055, 15)
league_type_1("2004a", 3070, 50, 40)
league_type_1("2004b", 3145, 50, 40)
league_type_1("2004c", 3220, 40, 40)
league_type_1("2004d", 3285, 25, 40)

transition("2005a", 3360, 15)
league_type_1("2005a", 3375, 50, 40)
league_type_1("2005b", 3450, 50, 40)
league_type_1("2005c", 3525, 40, 40)
league_type_1("2005d", 3590, 25, 40)

transition("2006a", 3665, 15)
league_type_1("2006a", 3680, 50, 40)
league_type_1("2006b", 3680+50+25, 50, 40)
league_type_1("2006c", 3680+50+25+50+25, 40, 40)
league_type_1("2006d", 3695+50+25+50+25+25+25, 25, 40)

transition("2007a", 3970, 15)
league_type_1("2007a", 3985, 50, 40)
league_type_1("2007b", 3985+50+25, 25, 40)

transition("2008a", 4135, 15)
league_type_1("2008a", 4150, 50, 40)
league_type_1("2008b", 4150+50+25, 25, 40)

transition("2009a", 4300, 15)
league_type_1("2009a", 4315, 50, 40)
league_type_1("2009b", 4315+50+25, 25, 40)

transition("2010a", 4465, 15)
league_type_1("2010a", 4480, 50, 40)
league_type_1("2010b", 4480+50+25, 25, 40)

transition("2011a", 4630, 15)
league_type_1("2011a", 4645, 50, 40)
league_type_1("2011b", 4645+50+25, 25, 40)

transition("2012", 4795, 15)
league_type_1("2012", 4810, 50, 40)
split("2012", 4885, 40, 2, 40)

transition("2013", 4975, 15)
league_type_1("2013", 4990, 50, 40)
split("2013", 4990+50+25, 40, 2, 40)

transition("2014", 5155, 15)
league_type_1("2014", 5170, 50, 40)
split("2014", 5245, 40, 2, 40)

transition("2015", 5335, 15)
league_type_1("2015", 5350, 50, 40)
split("2015", 5350+50+25, 40, 2, 40)

transition("2016", 5515, 15)
league_type_1("2016", 5530, 50, 40)
split("2016", 5530+50+25, 40, 2, 40)

transition("2017", 5700, 15)
league_type_1("2017", 5715, 50, 40)
split("2017", 5715+50+25, 40, 2, 40)

transition("2018", 5880, 15)
league_type_1("2018", 5910-15, 50, 40)
split("2018", 5910+50+25-15, 40, 2, 40)
'''
