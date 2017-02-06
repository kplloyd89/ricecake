import getopt, sys
import configparser
from ricecooker.classes import nodes, questions, files
from glob import glob
import os
import logging

rootfolder = False
SAMPLE_TREE = []

def child_meta_parse(path, id_master, id_multi):
    config = configparser.ConfigParser()
    config.read(path + "/metadata.ini")
    sub_path = glob(path + "/*")
    for i in sub_path:
        if i[-4:] == ".ini":
            i=None
    for x in config.sections():
        if path[-1] == "/":
            path = path[:-1]
        found = False
        node_path = []
        tparent = path
        while 1:
            tparent, folder = os.path.split(tparent)
            if folder == rootfolder:
                break
            if folder != "":
                node_path.append(folder)
        if len(node_path) > 1:
            del node_path[-2:]
        node_path.reverse()
        if len(node_path) > 0:
            p = SAMPLE_TREE
            z = 0
            while z < len(node_path):
                for t in p:
                    if (t["title"]):
                        if (t["title"] == node_path[z]):
                            if 'children' in t:
                                p = t["children"]
                                found = True
                                z += 1
                                break
                            else:
                                t["children"] = []
                                p = t['children']
                                found = True
                                z += 1
                                break
            c = dict(config[x])
            if 'license' in c:
                for i in sub_path:
                    if (os.path.isfile(i)):
                        filename, file_extension = os.path.splitext(i)
                        if file_extension == ".ini":
                            continue
                        tname, folder = os.path.split(filename)
                        if folder.lower() == c['title'].lower():
                            filepath = i
                            c['files'] = [{"path" : os.path.abspath(filepath)}]
            if 'title' in c:
                for i in sub_path:
                    if 'id' in c:
                        break
                    tname, folder = os.path.split(i)
                    c["title"] == folder.lower()
                    c['id'] = str(id_master) + id_multi
                    chr(ord(id_multi) + 1)
                    break
            p.append(c)
        else:
            for t in SAMPLE_TREE:
                if (t["title"]):
                    if (t["title"] == os.path.basename(os.path.dirname(path))):
                        if 'children' in t:
                            t["children"].append(dict(config[x]))
                            found = True
                            break
                        else:
                            t["children"] = []
                            t["children"].append(dict(config[x]))
                            found = True
                            break
    for i in sub_path:
        filename, file_extension = os.path.splitext(i)
        if (os.path.isdir(i)):
            child_meta_parse(i, id_master, id_multi)
            chr(ord(id_multi) + 1)

def meta_parse(path):
    id_master = 100
    id_multi = 'a'
    config = configparser.ConfigParser()
    config.read(path + "metadata.ini")
    print("Generating Root Structure")
    print("Found meta Data at: " + path + "metadata.ini")
    sub_path = glob(path + "/*")
    for i in sub_path:
        if i[-4:] == ".ini":
            i = None
    for x in config.sections():
        c = dict(config[x])
        if 'title' in c:
            for i in sub_path:
                if 'id' in c:
                    break
                else:
                    file, folder = os.path.split(i)
                    c["title"] == folder.lower()
                    c['id'] = str(id_master)+id_multi
                    id_master += 1
                    break
        if 'license' in c:
            for i in sub_path:
                if (os.path.isfile(i)):
                    filename, file_extension = os.path.splitext(i)
                    if file_extension == ".ini":
                        continue
                    tname, folder = os.path.split(filename)
                    if folder.lower() == c['title'].lower():
                        filepath = i
                        c['files'] = [{"path": os.path.abspath(filepath)}]
        SAMPLE_TREE.append(c)
    sub_path = glob(path + "/*/")
    for i in sub_path:
        if i[-4:] == ".ini":
            i=None
    for i in sub_path:
        if(os.path.isdir(i)):
            child_meta_parse(i, id_master, id_multi)
            chr(ord(id_multi) + 1)
    return SAMPLE_TREE
