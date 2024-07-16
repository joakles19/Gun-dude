import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
from matplotlib.animation import PillowWriter
from matplotlib.font_manager import FontProperties
import database

pixelfont = FontProperties(fname='pictures for survivor game/PixeloidMono-d94EV.ttf')

def create_plot(x,y,title,xlabel,ylabel,filename):
    figplot = plt.figure()
    axplot = plt.axes()
    plt.xlabel(xlabel,font=pixelfont)
    plt.ylabel(ylabel,font=pixelfont)
    plt.title(title,font=pixelfont)
    axplot.plot(x,y,color='#590001')
    axplot.set_facecolor('#ff4f61')
    figplot.set_facecolor('#5788eb')
    plt.savefig(f'Game analytics/{filename}')

def enemy_stemchart():
    figstem = plt.figure()
    axstem = plt.axes(projection='3d')

    data = database.enemy_information()
    enemies = []
    health = []
    damage = []
    speed = []
    for n in data:
        enemies.append(n[0])
        health.append(n[1])
        damage.append(n[2])
        speed.append(n[3])

    for t in range(0,len(data)):
        axstem.stem([health[t]],[speed[t]],[damage[t]],linefmt='Grey',markerfmt='o',label=enemies[t])
    axstem.legend()
    axstem.set_xlabel('Health',font=pixelfont)
    axstem.set_ylabel('Speed',font=pixelfont)
    axstem.set_zlabel('Damage',font=pixelfont)
    axstem.set_facecolor('#056109')
    figstem.set_facecolor('#056109')

    plt.savefig('Game analytics/Enemy stem chart.png')

def bar_chart(x,y,title,xlabel,ylabel,filename):
    figbar = plt.figure()
    axbar = plt.axes()
    plt.xlabel(xlabel,font=pixelfont)
    plt.ylabel(ylabel,font=pixelfont)
    plt.title(title,font=pixelfont)
    plt.grid(True,zorder=0)
    axbar.bar(x,y,hatch='+',color='#1100ff',edgecolor='Black',zorder=3)
    axbar.set_facecolor('#ff4f61')
    figbar.set_facecolor('#5788eb')
    plt.savefig(f'Game analytics/{filename}')

