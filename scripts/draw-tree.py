from ete3 import Tree, TreeStyle, faces, CircleFace, AttrFace, NodeStyle, TextFace
t = Tree()
# t.populate(30, names_library=range(30))
t = Tree('all-patric-and-crickmore.aa.1k.phy.proml.outtree')


    # vowels = set(["j1.2780"])
    # print("here")
    # if node.name in vowels:
    #
    #    # Note that node style are already initialized with the
    #    # default values
    #
    #    node.style["fgcolor"] = "red"
    #    # node.img_style["color"] = "red"

clades = dict()
hemiptera = [
              "2A", # multiple species
              "3A",
              "11A"
              ]

rhabditida = [
              "5A",
              "5B",
              "12A",
              "13A",
              "14A",
              "21A",
              "55A"
              ]

lepidoptera = [
               "1A",
               "1B",
               "1C",
               "1D",
               "1E",
               "1F",
               "1G",
               "1H",
               "1I",
               "1J",
               "1K",
               "2A", # multiple species
               "7B",
               "8D",
               "9A",
               "9B",
               "9C",
               "9E",
               "15A",
               "22A",
               "32A",
               "51A"
               ]

diptera =      [
                "1A",
                "1B",
                "1C",
                "2A",
                "4A",
                "4B",
                "1D",
                "11A",
                "11B",
                "16A",
                "19A",
                "19B",
                "20A",
                "24C",
                "27A",
                "32B",
                "32C",
                "32D",
                "39A",
                "44A",
                "47A",
                "48A",
                "49A"
               ]

coleoptera =   [
                "1B", #ALSO I OR L -> CHECK THIS
                "3A",
                "3B",
                "3C",
                "7A",
                "8A",
                "8B",
                "8C",
                "8D",
                "8E",
                "8F",
                "8G",
                "9D",
                "14A",
                "18A",
                "22A",
                "22B",
                "23A",
                "34A",
                "34B",
                "35A",
                "35B",
                "36A",
                "37A",
                "43A",
                "43B",
                "55A"
               ]

cancer =       [
                "31A",
                "41A",
                "42A",
                "45A",
                "46A",
               ]

gastropoda =    [
                "1Ab" # multiple species
               ]
hymenoptera =  [
                "3A",
                "5A",
                "22A"
               ]

def getColor(list, color):
    for cry in list:
        clades[cry] = color

# http://colorbrewer2.org/#type=qualitative&scheme=Pastel1&n=9
#fbb4ae
#b3cde3
#ccebc5
#decbe4
#fed9a6
#ffffcc
#e5d8bd
#fddaec
#f2f2f2

getColor(hemiptera, "gold")
getColor(gastropoda, "coral")
getColor(hymenoptera, "lightcyan")
getColor(cancer, "salmon")
getColor(rhabditida, "pink")
getColor(coleoptera, "plum")
getColor(lepidoptera, "lightgreen")
getColor(diptera, "lightblue")


def layout(node):
    if node.is_leaf():

        for key in clades:
            # print(key)
            # name = node.get_leaf_names()
                    # print name
                # for i, name in enumerate(set(node.get_leaf_names())):
                #     if name.startswith("Cry1A"):
                #         print("here")
                #         node.img_style["bgcolor"] = "#9db0cf"
            if key in node.name:
                node.img_style["bgcolor"] = clades[key]
            elif node.name.startswith("j") or \
                 node.name.startswith("a") or \
                 node.name.startswith("m") or \
                 node.name.startswith("s") or \
                 node.name.startswith("d"):
                node.img_style["bgcolor"] = "red"
            # elif "^C" not in node.name :
            #     node.img_style["bgcolor"] = "red"
                # if node.name == "j1.2780":
                # print(node)
                # changes the leaf name and colors it red
                # NOTE: set leaf name to False to make this work properly
                # node.name = "blah"
                # N = AttrFace("name", fgcolor = "red")
                # faces.add_face_to_node(N, node, 1, aligned=True)
                # node.img_style["bgcolor"] = "#9db0cf"

ts = TreeStyle()
ts.layout_fn = layout
ts.mode = "c"
ts.force_topology = True
# ts.scale
# ts.show_scale = False
# ts.branch_vertical_margin = 5
ts.scale = 23
ts.title.add_face(TextFace("ML Tree Representing Known Cry and Novel Cry Toxins", fsize=40), column=20)
ts.legend.add_face(TextFace("hemiptera", fsize=20, fgcolor="lightblue"), column=1)
ts.legend.add_face(TextFace("gastropoda", fsize=20, fgcolor="coral"), column=1)
ts.legend.add_face(TextFace("hymenoptera", fsize=20, fgcolor="lightcyan"), column=1)
ts.legend.add_face(TextFace("cancer", fsize=20, fgcolor="lightgreen"), column=1)
ts.legend.add_face(TextFace("rhabditida", fsize=20, fgcolor="salmon"), column=1)
ts.legend.add_face(TextFace("coleoptera", fsize=20, fgcolor="gold"), column=1)
ts.legend.add_face(TextFace("lepidoptera", fsize=20, fgcolor="plum"), column=1)
ts.legend.add_face(TextFace("diptera", fsize=20, fgcolor="pink"), column=1)
ts.legend.add_face(TextFace("novel cry", fsize=20, fgcolor="red"), column=1)
ts.legend_position=2
# ts.show_leaf_name = False
# t.show(tree_style=ts)

# for n in t.traverse:

t.render("test.pdf",tree_style=ts, w=10000, units="mm")
