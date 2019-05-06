import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient(ambient,areflect)
    d = limit_color(calculate_diffuse(light,dreflect,normal))
    s = limit_color(calculate_specular(light,sreflect,view,normal))
    # d = calculate_diffuse(light,dreflect,normal)
    # s = calculate_specular(light,sreflect,view,normal)
    # a = [0,0,0]
    # d = [0,0,0]
    # s = [0,0,0]
    # print(a)
    # print(d)
    # print(s)
    # print()
    # print(s)
      
    P = [a[0]+d[0]+s[0],a[1]+d[1]+s[1],a[2]+d[2]+s[2]]

    # print("s is: ",s)
    return limit_color(P)

def calculate_ambient(alight, areflect):
    amb = [0,0,0]
    for i in range(3):
      amb[i] = areflect[i] * alight[i]
    return amb

def calculate_diffuse(light, dreflect, normal):
    # print(light[LOCATION])
    p = dot_product(normal,light[LOCATION])
    # [-light[LOCATION][0],-light[LOCATION][1],-light[LOCATION][2]]
    # print("p is: ",p)
    dif = [0,0,0]
    for i in range(3):
      dif[i] = light[COLOR][i]*dreflect[i]*p
    return dif
    

def calculate_specular(light, sreflect, view, normal):
    c = dot_product(light[LOCATION],normal)
    proj = [n*c for n in normal]

    reflected = [0,0,0]
    for i in range(3):
      reflected[i] = 2 * proj[i] - light[LOCATION][i]

    normalize(reflected)
    power = 3
    r_vp = math.pow(dot_product(reflected,view),power)

    # if (r_vp > 0.5):
    #   print(light[LOCATION])
    spec = [0,0,0]
    for i in range(3):
      spec[i] = light[COLOR][i] * r_vp * sreflect[i]
    # print("s is: ",spec)
    return spec

def limit_color(color):
    for i in range(3):
      color[i] = int(color[i])
      if color[i] < 0:
        color[i] = 0
      if color[i] > 255:
        color[i] = 255
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    # print(vector)
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    # print("first vector is: ",a)
    # print("second vector is: ",b)
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
