from math import atan2, pi

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

if __name__ == "__main__":
    pie([0.33, 0.33, 0.34], ["My Thing", "Your Thing", "Other Thing"], r=8)
