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

def getTeams(year):
    fp = "/Users/hyungsoobae/Blender/{}_points.csv".format(year)
    result = []
    with open(fp) as csvfile:
        rdr = csv.reader(csvfile)
        for i, row in enumerate(rdr):
            print (row[0])
            result.append(models[row[0]])
    return result


def set_frames(year ,ffrom, incremental):
    fp = "/Users/hyungsoobae/Blender/{}_points.csv".format(year)
    with open(fp) as csvfile:
        rdr = csv.reader(csvfile)
        for i, row in enumerate(rdr):
            frame = ffrom
            
            team = models[row[0]]
            bpy.context.scene.frame_set(frame)
            
            team.scale[2] = 0
            team.keyframe_insert(data_path='scale') 

            logo = models['{}_Logo'.format(row[0])]
            logo.location[2] = team.scale[2] * 2 + 0.4
            logo.keyframe_insert(data_path='location')
            
            name = models['{}_Name'.format(row[0])]
            name.location[2] = logo.location[2] + 2
            name.keyframe_insert(data_path='location')
            
            models['{}_Point'.format(row[0])].location[2] = logo.location[2] - 1.2
            models['{}_Point'.format(row[0])].location[2] = 0
            models['{}_Point'.format(row[0])].keyframe_insert(data_path='location')
            
            
            models['{}_Point'.format(row[0])].data.text_counter_props.ifAnimated=True
            models['{}_Point'.format(row[0])].data.text_counter_props.counter = 0
            models['{}_Point'.format(row[0])].data.keyframe_insert(data_path='text_counter_props.counter')             
                
            frame += incremental
            
            for point in row[1:]:
                bpy.context.scene.frame_set(frame)
                team.scale[2] = 0 if float(point)/18 < 0 else float(point)/18
                
                team.keyframe_insert(data_path='scale')
                
                models['{}_Point'.format(row[0])].data.text_counter_props.ifAnimated=True
                models['{}_Point'.format(row[0])].data.text_counter_props.counter = int(point)
                models['{}_Point'.format(row[0])].data.keyframe_insert(data_path='text_counter_props.counter') 

                logo = models['{}_Logo'.format(row[0])]
                logo.location[2] = team.scale[2] * 2 + 0.4
                logo.keyframe_insert(data_path='location')
                
                name = models['{}_Name'.format(row[0])]
                name.location[2] = logo.location[2] + 2
                name.keyframe_insert(data_path='location')
                
                if team.scale[2] > 0.5:
                    models['{}_Point'.format(row[0])].location[2] = logo.location[2] - 1.2
                else:
                    models['{}_Point'.format(row[0])].location[2] = 0
                    
                models['{}_Point'.format(row[0])].keyframe_insert(data_path='location')
            
                frame += incremental
                
            sort_bars(year, ffrom, incremental)

    print ("set_frame :: Completed")

def sort_bars(year, ffrom, incremental):
    fp = "/Users/hyungsoobae/Blender/{}_ranking.csv".format(year)
    
    frame = ffrom
    bpy.context.scene.frame_set(frame)
    for team in getTeams(year):
        models[team.name].keyframe_insert(data_path='location')
        models["{}_Logo".format(team.name)].keyframe_insert(data_path='location')
        models["{}_Name".format(team.name)].keyframe_insert(data_path='location')   
        models["{}_Point".format(team.name)].keyframe_insert(data_path='location')

    
    with open(fp) as csvfile:
        rdr = csv.reader(csvfile)
        
        
        for i, row in enumerate(rdr):
            frame += incremental
            bpy.context.scene.frame_set(frame)

            for rank, team in enumerate(row[1:]):
                bpy.context.scene.frame_set(frame)
                
                models[team].location[0] = positions[rank][0]
                
                models["{}_Logo".format(team)].location[0] = positions[rank][0]
                models["{}_Logo".format(team)].location[2] = models[team].scale[2] * 2 + 0.4
                
                models["{}_Name".format(team)].location[0] = positions[rank][0]
                models["{}_Name".format(team)].location[2] = models["{}_Logo".format(team)].location[2] + 2
                
                models["{}_Point".format(team)].location[0] = positions[rank][0]                
                
                
                models[team].keyframe_insert(data_path='location')
                models["{}_Logo".format(team)].keyframe_insert(data_path='location')
                models["{}_Name".format(team)].keyframe_insert(data_path='location')   
                models["{}_Point".format(team)].keyframe_insert(data_path='location') 
            
    print ("sort_bars :: Completed")


def transition(ffrom, cyear, nyear, duration):
    frame = ffrom
    print (frame)
    
    current_teams = set(getTeams(cyear))
    print ("current", current_teams)
    
    next_teams = set(getTeams(nyear))
    print ("next", next_teams)
    
    if nyear == 1995:
        temp = -4
    elif nyear >= 1996:
        temp = -5
    else:
        temp = len(next_teams - current_teams) * -1
    
    
    for i,team in enumerate(next_teams - current_teams):
        bpy.context.scene.frame_set(frame)
        team.keyframe_insert(data_path='location')
        models["{}_Logo".format(team.name)].keyframe_insert(data_path='location')
        models["{}_Name".format(team.name)].keyframe_insert(data_path='location')
        models['{}_Point'.format(team.name)].keyframe_insert(data_path='location')
        
        
        bpy.context.scene.frame_set(frame+duration)
        team.location[0] = positions[temp+i][0]
        models["{}_Logo".format(team.name)].location[0] = positions[temp+i][0]
        models["{}_Name".format(team.name)].location[0] = positions[temp+i][0]
        models['{}_Point'.format(team.name)].location[0] = positions[temp+i][0]
        models["{}_Name".format(team.name)].location[2] = models["{}_Logo".format(team.name)].location[2] + 2
        models['{}_Point'.format(team.name)].location[2] = 0
                
        team.keyframe_insert(data_path='location')
        models["{}_Logo".format(team.name)].keyframe_insert(data_path='location')
        models["{}_Name".format(team.name)].keyframe_insert(data_path='location')
        models['{}_Point'.format(team.name)].keyframe_insert(data_path='location')
    
    for team in current_teams:
        
        bpy.context.scene.frame_set(frame)
        
        if team in (current_teams - next_teams):
            team.keyframe_insert(data_path='location')
        
        models['{}_Point'.format(team.name)].data.text_counter_props.counter = models['{}_Point'.format(team.name)].data.text_counter_props.counter
        
        team.keyframe_insert(data_path='scale')
        models["{}_Logo".format(team.name)].keyframe_insert(data_path='location')
        models["{}_Name".format(team.name)].keyframe_insert(data_path='location')
        models['{}_Point'.format(team.name)].data.keyframe_insert(data_path='text_counter_props.counter')
        models['{}_Point'.format(team.name)].keyframe_insert(data_path='location')        
        
        
        
        bpy.context.scene.frame_set(frame+duration)
        
        
        if team in current_teams - next_teams:
            team.location[0] = 50
            team.keyframe_insert(data_path='location')
            models["{}_Logo".format(team.name)].location[0] = 50
            models["{}_Name".format(team.name)].location[0] = 50
            models['{}_Point'.format(team.name)].location[0] = 50
          
        team.scale[2] = 0
        
        models["{}_Logo".format(team.name)].location[2] = models[team.name].scale[2] * 2 + 0.4
        models["{}_Name".format(team.name)].location[2] = models["{}_Logo".format(team.name)].location[2] + 2
        models['{}_Point'.format(team.name)].data.text_counter_props.counter = 0
        models['{}_Point'.format(team.name)].location[2] = 0
                
        models['{}_Point'.format(team.name)].keyframe_insert(data_path='location')        
        team.keyframe_insert(data_path='scale')
        models["{}_Logo".format(team.name)].keyframe_insert(data_path='location')
        models["{}_Name".format(team.name)].keyframe_insert(data_path='location')
        models['{}_Point'.format(team.name)].data.keyframe_insert(data_path='text_counter_props.counter')       
        
    
    
    
bpy.context.scene.frame_set(0)

models = bpy.data.objects
scn = bpy.context.scene

#Logo Size
'''
for model in models:
    if "_Logo" in model.name:
        model.scale[0] = 1.6
        model.scale[1] = 1.6
'''


for model in models:
    model.animation_data_clear()
    model.data.animation_data_clear()
    if "Point" in model.name:
        model.data.animation_data_clear()

        
positions = [(1.0, 0.0), (2.5999999046325684, 0.0), (4.199999809265137, 0.0), (5.800000190734863, 0.0), (7.400000095367432, 0.0), (9.0, 0.0), (10.600000381469727, 0.0), (12.199999809265137, 0.0), (13.800000190734863, 0.0), (15.399999618530273, 0.0), (17.0, 0.0), (18.600000381469727, 0.0), (20.200000762939453, 0.0), (21.799999237060547, 0.0), (23.399999618530273, 0.0), (25.0, 0.0), (26.600000381469727, 0.0), (28.200000762939453, 0.0), (29.799999237060547, 0.0), (31.399999618530273, 0.0), (33.0, 0.0), (34.599998474121094, 0.0)]

for team in getTeams(1992):
    team.location[0] = 50
    for model in models:
        if team.name in model.name:
            model.location[0] = 50
            
for i,team in enumerate(getTeams(2018)):
    team.location[0] = positions[i][0]
    models['{}_Logo'.format(team.name)].location[0] = positions[i][0]
    models['{}_Name'.format(team.name)].location[0] = positions[i][0]
    models['{}_Point'.format(team.name)].location[0] = positions[i][0]

set_frames(2018,0,50)
#set_frames(1992, 0, 10)
#transition(445, 1992, 1993, 15)
#set_frames(1993, 485, 10)
#transition(930, 1993, 1994, 15)
#set_frames(1994, 970, 10)
#transition(1415, 1994, 1995, 15)
#set_frames(1995, 1455, 10)
#transition(1860, 1995, 1996, 15)
#set_frames(1996, 1900, 10)
#transition(2305, 1996, 1997, 15)
#set_frames(1997, 2345, 10)


#transition(2750, 1997, 1998, 15)
#set_frames(1998, 2790, 10)
#transition(3195, 1998, 1999, 15)
#set_frames(1999, 3235, 10)
#transition(3640, 1999, 2000, 15)
#set_frames(2000, 3680, 10)
#transition(4085, 2000, 2001, 15)
#set_frames(2001, 4125, 10)
#transition(4530, 2001, 2002, 15)
#set_frames(2002, 4570, 10)
#transition(4975, 2002, 2003, 15)
#set_frames(2003, 5015, 10)
#transition(5420, 2003, 2004, 15)
#set_frames(2004, 5460, 10)
#transition(5865, 2004, 2005, 15)
#set_frames(2005, 5905, 10)
#transition(6310, 2005, 2006, 15)
#set_frames(2006, 6350, 10)
#transition(6755, 2006, 2007, 15)
#set_frames(2007, 6795, 10)
#transition(7200, 2007, 2008, 15)
#set_frames(2008, 7240, 10)
#transition(7645, 2008, 2009, 15)
#set_frames(2009, 7685, 10)
#transition(8090, 2009, 2010, 15)
#set_frames(2010, 8130, 10)
#transition(8535, 2010, 2011, 15)
#set_frames(2011, 8575, 10)
#transition(8980, 2011, 2012, 15)
#set_frames(2012, 9020, 10)
#transition(9425, 2012, 2013, 15)
#set_frames(2013, 9465, 10)
#transition(9870, 2013, 2014, 15)
#set_frames(2014, 9910, 10)
#transition(10315, 2014, 2015, 15)
#set_frames(2015, 10355, 10)
#transition(10760, 2015, 2016, 15)
#set_frames(2016, 10800, 10)
#transition(11205, 2016, 2017, 15)
#set_frames(2017, 11245, 10)
#transition(11650, 2017, 2018, 15)
#set_frames(2018, 11690, 10)


'''
notinmodel = set()
for year in range(1992,2018):
    fp = "/Users/hyungsoobae/Blender/{}_points.csv".format(year)
    with open(fp) as csvfile:
        rdr = csv.reader(csvfile)
        for i, row in enumerate(rdr):
            if row[0] not in models:
                notinmodel.add(row[0])

print (notinmodel)
'''

'''
for model in models:
    if "_Name" in model.name:
        model.data.size = 0.75
'''


'''
bpy.context.scene.frame_set(11220)
print (models['Year_Value_1'].data.text_counter_props.counter)
models['Year_Value_1'].data.keyframe_insert(data_path='text_counter_props.counter')
print (models['Year_Value_2'].data.text_counter_props.counter)
models['Year_Value_2'].data.keyframe_insert(data_path='text_counter_props.counter')


bpy.context.scene.frame_set(11665)
models['Year_Value_1'].data.text_counter_props.counter = models['Year_Value_1'].data.text_counter_props.counter + 1
models['Year_Value_1'].data.keyframe_insert(data_path='text_counter_props.counter')
models['Year_Value_2'].data.text_counter_props.counter = models['Year_Value_2'].data.text_counter_props.counter + 1
models['Year_Value_2'].data.keyframe_insert(data_path='text_counter_props.counter')
'''