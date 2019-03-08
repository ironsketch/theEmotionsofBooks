import os, node
colors = ["green", "blue", "violet", "crimson", "alabaster", "orange", "aqua", "amaranth", "purple", "pink", "red", "amber", "bronze", "brown", "gold", "rose", "silver", "yellow", "amethyst", "white", "brass", "fuchsia", "ruby", "aquamarine", "lime", "gray", "auburn", "azure", "batorange", "beige", "black", "blond", "blood", "sapphire", "lavender", "lilac", "maroon", "turquoise", "rose", "burgundy", "cadet", "cerulean", "charcoal", "chartreuse", "copper", "coral", "cyan", "ebony", "ultramarine", "firebrick", "garnet", "ivory", "indigo", "jade", "khaki", "magenta", "mahogany", "mauve", "olive", "opal", "periwinkle", "scarlet", "sienna", "tan", "teal", "topaz", "umber", "vermillion"]

nodes = []

def openFolder(userF):
    files = []
    for root, dirs, filenames in os.walk(userF):
        files = filenames
    return files

def findColors(files, userF):
    for f in files:
        location = ""
        if f[len(f) - 1] != "/":
            location = userF + "/" + f
        else:
            location = userF + "/" + f

        fh = open(location, "r")

        fh = fh.read()
        fh = fh.replace('\n', '')
        fh = fh.replace('\r', '')
        fh = fh.replace('\\', '')
        fh = fh.replace('!', '.')
        fh = fh.replace('?', '.')
        sen = fh.split('. ')

        for s in sen:
            s = s.replace('.', '')
            tmp = s.split(' ')
            for word in tmp:
                new = True
                if word in colors:
                    for each in nodes:
                        if word in each:
                            each[1].colorAgain(word, tmp)
                            new = False
                    if new:
                        nodes.append([word, node.color(word, tmp)])

def main():
    userF = "books/"
    files = openFolder(userF)
    findColors(files, userF)
    for each in nodes:
        each[1].getColorLoc()

main()
