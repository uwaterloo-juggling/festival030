""" Util to draw juggling ladder diagrams. """

import math
import argparse

import numpy as np
import cairo


"""
COLORS = {
    "orange": rgba("#fe9920"),
    "red": rgba("#e54b4b"),
    "blue": rgba("#5aa9e6"),
    "white": rgba("#e4fde1"),
    "grey": rgba("#303030"),
    "black":rgba("#030303"),
}"""
COLORS = {}


def rgba(c):
    ''' Convert from named color or hex code to rgba. '''
    hx = COLORS[c] if c in COLORS else c
    hx = hx.lstrip("#").upper()
    r,g,b = tuple(int(hx[i:i+2], 16)/256 for i in (0, 2, 4))
    return (r,g,b,1.0)

parser = argparse.ArgumentParser(description="Generate ladder diagrams")
parser.add_argument("--siteswap", default="534")
parser.add_argument("--margin", default=10, type=float)
parser.add_argument("--beat-spacing", default=10, type=float)
parser.add_argument("--track-spacing", default=10, type=float)
parser.add_argument("--line-width", default=2, type=float)
parser.add_argument("--default-color", default="#00FFFF") # default color
parser.add_argument("--colors", default=[],
    type = lambda x: x.split(","))
parser.add_argument("--repeat", default=100, type=int) # use total_beats instead
parser.add_argument("--total-beats",default=0,type=int) # include how many beats
parser.add_argument("--palette",default="palette.txt")
parser.add_argument("--out",default="diagram.svg")
args = parser.parse_args()

# Some globals (sorry)
ORIGIN = (0,0)
ctx = None

def gen_dots(n_beats = 10):
    i = np.arange(n_beats)
    x = ORIGIN[0] + i*args.beat_spacing/2
    y = ORIGIN[1] + (i%2) * args.track_spacing 
    return np.column_stack([x,y])

def draw_throw_from(start,end,color=None):
    # Line settings
    ctx.set_line_width(args.line_width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    if color:
        ctx.set_source_rgba(*rgba(color))
    else:
        ctx.set_source_rgba(*rgba(args.default_color))

    # Draw the line
    if start[1] != end[1] or start[0] == end[0]:
        # odd throw or 0
        ctx.move_to(*start)
        ctx.line_to(*end)
        ctx.stroke()
    else:
        # same-hand throw.
        # Use as bezier cuve control point
        mid = ((start[0] + end[0])/2, ORIGIN[1] + args.track_spacing/2)
        ctx.move_to(*start)
        ctx.curve_to(mid[0],mid[1],mid[0],mid[1],end[0],end[1])
        ctx.stroke()

def draw_pattern(colors=[None]):
    # TODO better siteswap parsing
    siteswap = [int(ch) for ch in args.siteswap]

    # TODO Calculate n dynamically to guarantee repeat/tiling
    siteswap = siteswap*(args.repeat*3) # *3 to overlap the left and right side

    global ORIGIN
    ORIGIN = (-1*args.repeat*args.beat_spacing, args.margin)

    dots = gen_dots(n_beats = len(siteswap))
    colors += [None] * (len(siteswap) - len(colors))
    for i, value in enumerate(siteswap):
        if i + value < len(siteswap):
            draw_throw_from(dots[i], dots[i+value], color=colors[i])
            colors[i+value] = colors[i] # "throw" ball of given color

if __name__=="__main__":
    args = parser.parse_args()

    # Load colour palette if specified
    if args.palette:
        with open(args.palette,"r") as f:
            for line in f.readlines():
                name,hex = line.split()
                COLORS[name] = hex

    # Calculate dimensions
    if args.total_beats > 0:
        width = args.total_beats * args.beat_spacing
    else:
        width = args.repeat * len(args.siteswap) * args.beat_spacing
    height = 2*args.margin + args.track_spacing 

    if args.out[-4:] == ".svg":
        svg = args.out
    else:
        svg = "temp.svg"

    with cairo.SVGSurface(svg,width,height) as surface:
        ctx = cairo.Context(surface)
        
        draw_pattern(colors=args.colors)
        
        if args.out[-4:] == ".png":
            surface.write_to_png(args.out)
