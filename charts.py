import time
from math import atan2, pi, atan, ceil
import ctypes
import sys
import os

colors = [ 
    #"\033[30m█",  # Black..............
    "\033[31m█",  # Red                
    "\033[36m█",  # Cyan               
    "\033[32m█",  # Green              
    "\033[35m█",  # Magenta            
    "\033[33m█",  # Yellow             
    "\033[34m█",  # Blue               
    "\033[37m█",  # White              
    "\033[91m█",  # Bright Red         
    "\033[92m█",  # Bright Green       
    "\033[93m█",  # Bright Yellow      
    "\033[94m█",  # Bright Blue        
    "\033[95m█",  # Bright Magenta     
    "\033[96m█",  # Bright Cyan        
    "\033[97m█"   # Bright White       
]


def windows_enable_unicode_and_ansi():
    if os.name == 'nt': # for Bimbows
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11) # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0001 | 0x0004)  # ENABLE_PROCESSED_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING

        sys.stdout.reconfigure(encoding='utf-8')

def pie(v, labels, r):
    # Base implementation from https://codegolf.stackexchange.com/questions/23350/ascii-art-pie-chart
    mult = (1 / sum(v))
    for i in range(len(v)):
        v[i] *= mult

    v[-1] += 0.00000001

    def s(k,v,a):
        if not v:
            return ' '
        if a<v[0]:
            return k[0]
        return s(k[1:], v[1:], a-v[0])

    i = -2
    for y in range(-r, max(r, len(v)*2)):
        t=""
        if y < r:
            for x in range(-r,r):
                if x*x + y*y < r*r:
                    a = atan2(y,x)/pi/2 + 0.5
                    t += s(colors,v,a) * 2
                else:
                    t += "  "
        else:
            t += "  " * r * 2

        if i < len(labels)*2:
            if i >= 0 and i%2 == 0:
                percentage = v[i//2] * 100
                t += "   " + colors[i//2] + "\033[0m " +  f"{percentage:.2f}% " + labels[i//2]
            i += 1

        print(t)

    print("\033[0m")


def bresenham_line(matrix, width, height, start, end):
    """Draw line in matrix with Bresenham: https://en.wikipedia.org/wiki/Bresenham's_line_algorithm"""
    x1, y1 = start
    x2, y2 = end

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    up_slope = "／"
    down_slope = "＼"
    if os.name == 'nt': #compensate for shitty unicode support on windows
        down_slope = "\\_"
        up_slope = "_/"


    while True:
        slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
        
        char = "xx"
        err2 = err * 2
        erry = err
        if err2 > -dy:
            err -= dy
            erry = err
            x1 += sx

        if err2 < dx:
            err += dx
            y1 += sy

        if slope < 0:
            if err*2 < -dy:
                char = "__"
            elif err*2 > dx or err2 > dx:
                char = "| "
            else:
                char = up_slope
        else:
            if err2 < -dy:
                char = "__"
            elif err*2 > dx or err2 > dx:
                char = "| "
            else:
                char = down_slope

        if 0 <= x1 < height and 0 <= y1 < width:
            matrix[x1][y1] = "\033[31m" + char + "\033[0m"

        if x1 == x2 and y1 == y2:
            break


def line(labels, xs, ys, w, h, div_n, vpadding):
    div_h = h // (div_n+1)
    w //= 2
    max_y = max(ys)
    min_y = min(ys)

    bottom = min_y - vpadding
    top = max_y + vpadding

    fy = 0
    if max(ys) != 0:
        fy = (h-1) / (top-bottom)

    ys = list(map(lambda y: round((y-bottom)*fy), ys))
    ys = list(map(lambda y: round((top-bottom)*fy-y), ys))

    maxx = w/(max(xs))
    xs = list(map(lambda x: int((x-min(xs)) / (max(xs) - min(xs)) * w), xs))

    screen = []

    for i in range(h):
        row = []
        row.append("| ")
        if i%div_h == 0:
            if (i == 0):
                for j in range(w):
                    row.append("  ")
            else:
                for j in range(w):
                    color = "\033[30m"
                    if os.name == 'nt':
                        color = "\033[37m"
                    row.append(color + "__\033[0m")
            row.append("|")
            value = ((top-bottom) * (1-(i/h))) + bottom 
            row.append(f"{value:.2f}")
        else:
            for j in range(w):
                row.append("  ")
            row.append("|")
        screen.append(row)
    
    screen.append(["|_"] + ["__"]*w + [f"|{bottom:.2f}"])
    row = ["  "]*w
    for x1 in xs[:-1]:
        row[x1] = "| "
    row.append("  ")
    row.append("| ")
    screen.append(row)
    spacing = w*2//(len(labels)-1)- len(labels[0])

    while spacing < 1:
        labels = labels[::2]
        spacing = w*2//(len(labels)-1)- len(labels[0])

    row = [] 
    row.append("|"+labels[0])
    previous = len(labels[0])
    for i, label in enumerate(labels):
        spacing = (xs[i]*2) - previous
        if spacing > 2:
            row.append(" "*(spacing-1))
            row.append("| "+ label)
            previous = (xs[i]*2) + len(label)

    screen.append(row)

    for index in range(0, len(ys)-1):
        x1 = xs[index]
        x2 = xs[index+1]
        y1 = ys[index]
        y2 = ys[index+1]
        bresenham_line(screen, w+1, h, (y1, x1), (y2, x2))
        if index == 0:
            screen[y1][x1] = "|x"
        else:
            screen[y1][x1] = "xx"
    screen[y2][x2] = "xx"

    print("__"*(w+1))
    for y, row in enumerate(screen):
        r = ""
        for x, value in enumerate(row):
            r+=value
        print(r)

def bar(vals: list, labels: list, w, h, div_n):
    div_h = (h // (div_n-1))
    w //= 2
    max_y = ceil(max(vals))
    screen = []

    bar_space = w//len(vals)
    
    current_div_val = max_y
    for i in range(h):
        row = []
        row.append("| ")

        if i%div_h == 0:
            color = "\033[30m"
            if os.name == 'nt':
                color = "\033[37m"
            char = "  " if i == 0 else color + "__\033[0m"
            for j in range(w):
                row.append(char)

            row.append("|")
            row.append(f"{current_div_val:.2f}")
            current_div_val -= (max_y / div_n)
        else:
            for j in range(w):
                row.append("  ")
            row.append("|")

        screen.append(row)

    screen.append(["|_"] + ["__"]*w + [f"|{0:.2f}"])

    padding = 2
    if bar_space <= 2:
        padding = 0
    elif bar_space <= 4:
        padding = 1

    for i, v in enumerate(vals):
        for x in range(i*bar_space+padding, (i+1)*bar_space-padding):
            for y in range(h, (h-int((vals[i]/max_y)*h)),-1):
                screen[y][x+1] = colors[i]*2+"\033[0m"


    for y, row in enumerate(screen):
        for x, value in enumerate(row):
            print(value, end="")
        print("")

    print("")
    
    size = 0
    for i, l in enumerate(labels):
        bit = "  " + colors[i] + "\033[0m " + l + " "*((bar_space*2) - len(l) - 4)
        if (size + len(bit)) > w*4:
            print("")
            size = 0
        size += len(bit)
        print(bit, end="")
    print("")



if __name__ == "__main__":
    windows_enable_unicode_and_ansi()

    pie([0.33, 0.33, 0.33], ["My Thing", "Your Thing", "Other Thing"], r=8)
    
    print("")

    line(ys=[2, 0.5, 3, 0.1, 2, 5], w=80, h=20, div_n=4)

    print("\n")

    bar([2, 4.5, 3.2, 0.99], labels=["ahhh", "pup", "messi", ":)"], w=80, h=20, div_n=4)

    print("")
