import time
from math import atan2, pi, atan

def pie(v, labels, r):

    def s(k,v,a):
        if not v:
            return ' '
        if a<v[0]:
            return k[0]
        return s(k[1:], v[1:], a-v[0])

    colors = [ 
        "\033[30m█",  # Black..............
        "\033[31m█",  # Red                
        "\033[36m█",  # Cyan               
        "\033[33m█",  # Yellow             
        "\033[34m█",  # Blue               
        "\033[32m█",  # Green              
        "\033[35m█",  # Magenta            
        "\033[37m█",  # White              
        "\033[91m█",  # Bright Red         
        "\033[92m█",  # Bright Green       
        "\033[93m█",  # Bright Yellow      
        "\033[94m█",  # Bright Blue        
        "\033[95m█",  # Bright Magenta     
        "\033[96m█",  # Bright Cyan        
        "\033[97m█"   # Bright White       
    ]

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
                t += "   " + colors[i//2] + "\033[0m " + labels[i//2]
            i += 1

        print(t)

    print("\033[0m")


def bresenham_line(matrix, start, end):
    """Draw a line in the matrix from start to end coordinates using Bresenham's algorithm."""
    x1, y1 = start
    x2, y2 = end

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

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
                char = "_/"
                char = "／"
        else:
            if err2 < -dy:
                char = "__"
            elif err*2 > dx or err2 > dx:
                char = "| "
            else:
                char = "\_"
                char = "＼"

        if 0 <= x1 < len(matrix) and 0 <= y1 < len(matrix[0]):
            matrix[x1][y1] = char
        
        if x1 == x2 and y1 == y2:
            break
        

def line(ys, w, h):
    w //= 2
    ys = list(map(lambda y: max(ys)-y, ys))

    maxx = w/(len(ys)-1)
    fy = (h-1)/max(ys)

    ys = list(map(lambda y: round(y*fy), ys))

    screen = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append("  ")
        screen.append(row)

    for index in range(0, len(ys)-1):
        x1 = round(index*maxx) 
        x2 = round((index+1)*maxx)
        y1 = ys[index]
        y2 = ys[index+1]
        bresenham_line(screen, (y1, x1), (y2, x2))

    print("__"*(w+1))
    for y, row in enumerate(screen):
        r = ""
        for x, value in enumerate(row):
            r+=value
        print("|", end="")
        print("\033[31m"+r+"\033[0m", end="")
        print("|")
    print("--"*(w+1))



    # if 0:
    #     for y in range(0, h):
    #         t = ""
    #         for x in range(0, w):
    #                     if y == int(yval):
    #                         t+= "\033[31m██"
    #                         break
    #             else:
    #                 t += ".."
    #         print(t)



if __name__ == "__main__":
    pie([0.33, 0.33, 0.34], ["My Thing", "Your Thing", "Other Thing"], r=8)

    line(ys=[2, 0.5, 3, 0.1, 2, 5], w=80, h=20)
