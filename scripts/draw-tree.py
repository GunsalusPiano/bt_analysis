from ete3 import Tree, TreeStyle, faces, CircleFace, AttrFace, NodeStyle, TextFace, RectFace, Face
t = Tree()
t = Tree('all-patric-and-crickmore.clustered.aa.600.phy.proml.outtree')


clades = dict()

rhabditida = [
              "5Ca",
              "5Ea",
              "5Da",
              "6Aa",
              "5Ba",
              "55Aa"
              ]

lepidoptera = [
               "1Fa",
               "1Ad",
               "1Aa",
               "1Ca",
               "1Ea",
               "7Ba",
               "1Gc",
               "1Ac",
               "1Da",
               "1Ia",
               "1Id",
               "2Aa",
               "1Ja",
               "9Ea",
               "1Ba",
               "1Ab",
               "2Ab",
               "9Eb",
               "1Ie",
               "1Jc",
               "1Hb",
               # "1B",
               "1Bb",
               "2Ad",
               "1Db",
               "1Cb",
               "9Aa",
               "9Da",
               "1Ib",
               "1Bd",
               "1Ae",
               "1Fb",
               "1Ga",
               "1Ka",
               "9Ba",
               "1Gb",
               "2Ac"
               ]

diptera =      [
                "11Bb",
                "4Ba",
                "10Aa",
                "11Aa",
                "4Aa",
                "60Aa",
                "60Ba",
                "19Aa",
                "11Ba",
                "24Aa",
                "25Aa",
                "30Ca",
                "30Fa",
                "54Aa",
                "69Aa",
                "4Cc",
                "27Aa",
                "20Ba",
                "19Ba",
                "29Aa",
                "20",
                "30Aa",
                "1Ab",
                "4Cb",
                "56Aa",
                "30Ga",
                "30Ea"
               ]

coleoptera =   [
                "37Aa",
                "8Ma",
                "23Aa",
                "3Aa",
                "8Ia"
               ]

def getColor(list, color):
    for cry in list:
        clades[cry] = color

getColor(rhabditida, "mediumspringgreen")
getColor(coleoptera, "plum")
getColor(lepidoptera, "lightgreen")
getColor(diptera, "lightblue")

ts = TreeStyle()
# ts.layout_fn = layout
for node in t.traverse():
    node.img_style['size'] = 0
    if node.is_leaf():
        if node.name.startswith('C'):
            node.img_style['size'] = 5
        elif node.name.startswith('j'):

            # node.img_style['size'] = 5
            # node.img_style['fgcolor'] = "red"
            # node_face = RectFace(10,20, fgcolor="red", bgcolor="red")
            # node_face.inner_border = 1
            node.add_face(TextFace("Blah", inner_border_type=0), column=0)

ts.mode = "c"
ts.force_topology = True
ts.scale = 9
ts.title.add_face(TextFace("ML Tree Representing Known Cry and Novel Cry Toxins"), column=1)


t.render("test.pdf",tree_style=ts, w=10000, units="mm")
