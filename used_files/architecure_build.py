from operator import itemgetter
import xml.etree.ElementTree as ET
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", default="", help="")
parser.add_option("-o", "--output", dest="output", default="", help="")
parser.add_option("-n", "--name", dest="name", default="", help="")
(options, args) = parser.parse_args();




def main(path,outpath,name):
        xmltree = ET.parse(path) 
        root = xmltree.getroot()
        infodump = 0
        set_dic = {}
        if root.attrib["direction"] == "single-->set":
                out = open(outpath, "w")
                for protein in root:
                        if protein.tag == "single_protein":
                                infodump = (protein.attrib["id"], 0, [])
                for protein in root:
                        if protein.tag == "set_protein":
                                pid = protein.attrib["id"]
                                p_features = []
                                path = []
                                for arc in protein:
                                        if arc.tag == "architecture":
                                                for feature in arc:
                                                        ftype = feature.attrib["type"]
                                                        weight = feature.attrib["weight"]
                                                        for instance in feature:
                                                                out.write(name + "#" + pid + "#" + infodump[0] + "\t" + pid + "\t" + str(ftype) + "\t" + str(instance.attrib["start"]) + "\t" + str(instance.attrib["end"]) + "\t" + str(weight) + "\n")
                                        elif arc.tag == "path":
                                                for feature in arc:
                                                        ftype = feature.attrib["type"]
                                                        weight = feature.attrib["corrected_weight"]
                                                        for instance in feature:
                                                                out.write(name + "#" + pid + "#" + infodump[0] + "\t" + infodump[0] + "\t" + str(ftype) + "\t" + str(instance.attrib["start"]) + "\t" + str(instance.attrib["end"]) + "\t" + str(weight) + "\n")
        elif root.attrib["direction"] == "set-->single":
                out = open(outpath + "_1.domains", "w+")
                for protein in root:
                        if protein.tag == "single_protein":
                                arctmp = []
                                for feature in protein:
                                        ftype = feature.attrib["type"]
                                        weight = feature.attrib["weight"]
                                        for instance in feature:
                                                arctmp.append((protein.attrib["id"] + "#","#" + protein.attrib["id"] + "\t" + protein.attrib["id"] + "\t" + str(ftype) + "\t" + str(instance.attrib["start"]) + "\t" + str(instance.attrib["end"]) + "\t" + str(weight) + "\n"))
                                infodump = (protein.attrib["id"], 0, arctmp)
                for protein in root:
                        if protein.tag == "set_protein":
                                tmp = protein.attrib["id"]
                                tmp = tmp.split("|")
                                pid = tmp[1] + "_" + tmp[2]
                                p_features = []
                                path = []
                                for arc in protein:
                                        if arc.tag == "architecture":
                                                for line in infodump[2]:
                                                        out.write(line[0] + pid + line[1])
                                        elif arc.tag == "path":
                                                for feature in arc:
                                                        ftype = feature.attrib["type"]
                                                        weight = feature.attrib["corrected_weight"]
                                                        for instance in feature:
                                                                out.write(infodump[0] + "#" + pid + "#" + infodump[0] + "\t" + pid + "\t" + str(ftype) + "\t" + str(instance.attrib["start"]) + "\t" + str(instance.attrib["end"]) + "\t" + str(weight) + "\n")
        out.close

main(options.input, options.output, options.name)
