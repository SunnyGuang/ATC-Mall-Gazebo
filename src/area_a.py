import os
from data_class import Data_class
import numpy as np

# parameters:

start_time = 677300
end_time = 679400

max_peds = 50

db="/home/sunny/Downloads/atc-20121024.db"
a = Data_class(db)

actor_array = np.empty([91,1])
actor_list = actor_array.tolist()


def ad_x(x):
    return round((x/1000), 3) * 120.6/140 - 5 #(rate: 120.6/140)

def ad_y(y):
    return round((y/1000), 3) * 53.6/60 + 8 # (rate: 53.6/60)

actor_list[0][0] = [9190600, ad_x(-36668.0), ad_y(-3155.0),-3.073]
actor_list[1][0] = [9190700, ad_x(26636.0), ad_y(-15107.0),3.095]
actor_list[2][0] = [9190802, ad_x(-22342.0), ad_y(1687.0),-1.358]
actor_list[3][0] = [9194800, ad_x(3658.0), ad_y(-320.0),-0.401]
actor_list[4][0] = [9200100, ad_x(42021.0), ad_y(-17560.0),-0.914]
actor_list[5][0] = [9201900, ad_x(46605.0), ad_y(-22013.0),1.644]

#initial used_list and unused_list
used_list = []
used_list_ped = []
for i in range(6):
    used_list.append([i, actor_list[i][0][0]]) 
    used_list_ped.append(actor_list[i][0][0])

unused_list = []
for i in range(85):
    unused_list.append(i+6)
    actor_list[i+6][0]=([200, 200, 200,200])

for i in range(start_time, end_time):
    data = []
    data = a.extract_timewin_at(i)
    # initial and insert check_list
    check_list = []
    for k in range(len(data)):
        check_list.append(data[k][2])
        if check_list[k] not in used_list_ped:
            used_list.append([unused_list[0],data[k][2]])
            used_list_ped.append(data[k][2])
            unused_list.remove(unused_list[0])
    z = []
    # check used_list
    for j in used_list:
        if j[1] in check_list:
            z.append(j)
        else:
            used_list_ped.remove(j[1])
            unused_list.append(j[0])
            unused_list.sort()
    used_list = z 

    for k in range(len(used_list)):
        actor_list[used_list[k][0]].append([round(data[k][2],0), ad_x(data[k][3]), ad_y(data[k][4]), round(data[k][8],3)])
    
    for k in range(len(unused_list)):
        actor_list[unused_list[k]].append([200, 200, 200,200])

def smooth_data(data):
    smoothed_data = np.copy(data)

    for i in range(len(smoothed_data)):
        for j in range(len(smoothed_data[i])):
            if abs(smoothed_data[i][j][1]) == 200:
                continue
            # if ped is in the map
            elif abs(smoothed_data[i][j][1]) != abs(200) and abs(smoothed_data[i][j-1][1]) != abs(200):
                # compare x
                if abs(smoothed_data[i][j][1] - smoothed_data[i][j-1][1]) > 0.2 and smoothed_data[i][j-1][1] != 200:
                    # print(smoothed_data[i][j][0],smoothed_data[i][j][1], smoothed_data[i][j-1][1])
                    smoothed_data[i][j][1] = smoothed_data[i][j-1][1] + 0.1 * np.sign(smoothed_data[i][j][1] - smoothed_data[i][j-1][1])
                else:
                    smoothed_data[i][j][1] = smoothed_data[i][j][1]
                # compare y
                if abs(smoothed_data[i][j][2] - smoothed_data[i][j-1][2]) > 0.2 and smoothed_data[i][j-1][2] != 200:
                    smoothed_data[i][j][2] = smoothed_data[i][j-1][2] + 0.1 * np.sign(smoothed_data[i][j][2] - smoothed_data[i][j-1][2])
                else:
                    smoothed_data[i][j][2] = smoothed_data[i][j][2]
                # compare facing angle
                if abs(smoothed_data[i][j][3] - smoothed_data[i][j-1][3]) > 0.2 and smoothed_data[i][j-1][3] != 200:
                    smoothed_data[i][j][3] = smoothed_data[i][j-1][3] + 0.1 * np.sign(smoothed_data[i][j][3] - smoothed_data[i][j-1][3])
                else:
                    smoothed_data[i][j][3] = smoothed_data[i][j][3]
    return smoothed_data

actor_list = smooth_data(actor_list)

actor_list = actor_list.tolist()

def diff(a,b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2], a[3]-b[3]]
for i in range(500):
    print(diff(actor_list[0][i],actor_list[0][i+1]))

f = open("ped.world","a")
f.write('<?xml version="1.0" ?>')
f.write('\n<sdf version="1.5">')
f.write('\n  <world name="default">')
f.write('\n    <include>')
f.write('\n      <uri>model://ground_plane</uri>')
f.write('\n    </include>')
f.write('\n    <include>')
f.write('\n      <uri>model://sun</uri>')
f.write('\n    </include>')
f.write('\n    <include>')
f.write('\n      <uri>model://Area_A</uri>')
f.write('\n    </include>\n')
f.close()

for j in range(max_peds):
    f = open("ped.world","a")
    c = '\n    <actor name="actor%d">'%(j+1)
    f.write(c)
    f.write('\n      <pose>200 200 0 0 0 0</pose>')
    f.write('\n      <skin>')
    f.write('\n        <filename>moonwalk.dae</filename>')
    f.write('\n        <scale>1.0</scale>')
    f.write('\n      </skin>')
    f.write('\n      <animation name="walking">')
    f.write('\n        <filename>walk.dae</filename>')
    f.write('\n        <scale>1.000000</scale>')
    f.write('\n        <interpolate_x>true</interpolate_x>')
    f.write('\n      </animation>')
    f.write('\n      <script>')
    f.write('\n        <loop>false</loop>')
    f.write('\n        <delay_start>0</delay_start>')
    f.write('\n        <auto_start>true</auto_start>')
    f.write('\n        <trajectory id="0" type="walking">\n')
    f.close()
    #initial state:
    if actor_list[j][1][1] == 200:
        c1="\n          <waypoint>"
        c2="\n              <time>0.08</time>"
        c3="\n              <pose>200 200 -5 0 0 0</pose>"
        c4="\n          </waypoint>\n"
        c = c1 + c2 + c3 + c4
        f = open("ped.world","a")
        f.write(c)
        f.close()

    for i in range(len(actor_list[j])-1):

        # case appear actor:
        if (actor_list[j][i][1] == 200) and (actor_list[j][i+1][1]!=200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%(i/25+0.04)
            c3="\n              <pose>200 200 -5 0 0 0</pose>"
            c4="\n          </waypoint>\n"

            c = c1 + c2 + c3 + c4
            b1="\n          <waypoint>"
            b2="\n              <time>%g</time>"%((i)/25+0.038)
            b3="\n              <pose>%g %g -5 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            b4="\n          </waypoint>\n"

            b5="\n          <waypoint>"
            b6="\n              <time>%g</time>"%((i)/25+0.04)
            b7="\n              <pose>%g %g 0 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            b8="\n          </waypoint>\n"
            b = b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8

            f = open("ped.world","a")
            f.write(c)
            f.write(b)
            f.close()

        #case disappear actor:
        if (actor_list[j][i][1] != 200) and (actor_list[j][i+1][1]==200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%(i/25 + 0.001)
            c3="\n              <pose>%g %g -5 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            c4="\n          </waypoint>\n"

            c5="\n          <waypoint>"
            c6="\n              <time>%g</time>"%(i/25 + 0.04)
            c7="\n              <pose>200 200 0 0 0 0</pose>"
            c8="\n          </waypoint>\n"
            c = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8
            f = open("ped.world","a")
            f.write(c)
            f.close()

        if (actor_list[j][i][1]!=200) and (actor_list[j][i+1][1]!=200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%((i)/25+0.04)
            c3="\n              <pose>%g %g 0 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            c4="\n          </waypoint>\n"
            c = c1 + c2 + c3 + c4
            f = open("ped.world","a")
            f.write(c)
            f.close()     

    # final state:
    if actor_list[j][1][1] == 200:
        time_diff = end_time - start_time
        c1="\n          <waypoint>"
        c2="\n              <time>%g</time>"%(time_diff/25+0.04)
        c3="\n              <pose>200 200 -5 0 0 0</pose>"  
        c4="\n          </waypoint>\n"
        c = c1 + c2 + c3 + c4
        f = open("ped.world","a")
        f.write(c)
        f.close()

    
    f = open("ped.world","a")
    f.write('\n        </trajectory>')
    f.write('\n      </script>')
    f.write('\n    </actor>\n')
    f.close()

f = open("ped.world","a")
f.write('  </world>')
f.write('\n</sdf>')
f.close()