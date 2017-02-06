import getopt, sys
import configparser
from ricecooker.classes import nodes, questions, files
from .node_constructor import meta_parse
from . import ricewrapper
from glob import glob
import os
import logging
import shutil
import json
import subprocess

opath = False
rootfolder = False
SAMPLE_TREE = []

def main():
    print(os.environ['PATH'])
    Token = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "token=", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        #usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            #usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-token", "--token"):
            output = a
            Token = a
        else:
            assert False, "unhandled option"
    # ...
    if Token == False:
        print("You must enter a Token format: --token=<token>")
        sys.exit(2)
    if len(args) != 1:
        print("Proper Format is ricecake --token=<token> <folder_root_path>")
        sys.exit(2)
    print("Your Token is: ", Token)
    print(args[0])
    opath = args[0]# + "/channelmetadata.ini"
    #Time to parse!
    master_node_tree = create_node(opath)
    unique_data = create_temp_py(opath, master_node_tree)
    s = subprocess.check_output(['python','-m', 'ricecooker', 'uploadchannel', unique_data, '--token='+Token],
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE
                                )
    # Remove our file. I did not use tempfile because I want to add an option to keep the file for user debugging
    os.remove(unique_data)
    print("Ended without error!")

def create_node(path):
    junk, rootfolder = os.path.split(path)

    #folders_list = [x[0] for x in os.walk(path)]
    d = path
    root_path = glob(path + "/*/")
    print(root_path)
    if len(root_path) != 1:
        print("There MUST be only one folder in your target path along side your channelmetadata.ini")
        sys.exit(2)
    my_node_tree = meta_parse(root_path[0])
    LOG_FILENAME = 'example.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    logging.debug(my_node_tree)

    #_build_tree(channel, SAMPLE_TREE)
    #raise_for_invalid_channel(channel)

    return my_node_tree

def create_temp_py(path, tree):
    config = configparser.ConfigParser()
    config.read(path + "/channelmetadata.ini")
    print("Channel Meta Data Path: " + path + "/channelmetadata.ini")
    source_domain=config['channeldata']['domain'],
    source_id=config['channeldata']['source_id'],
    title=config['channeldata']['title'],
    thumbnail=config['channeldata'].get('thumbnail', None)
    temp = open('test.py', 'w')
    outline = open("ricewrapper.py", "r")
    shutil.copyfileobj(outline, temp)
    #ntree = ''.join('{}{}'.format(key, val) for key, val in tree.items())
    ntree = json.dumps(tree)
    #ntree - json.loads(ntree)
    temp.write("SAMPLE_TREE = ")
    temp.writelines(ntree)
    temp.write("\nchanneldata = {}")
    for l in config['channeldata']:
        str = "channeldata['"+l+"'] = '"+config["channeldata"][l]+"'"
        temp.write("\n"+str)
    return temp.name

if __name__ == "__main__":
    main()


    # Currently my program creates a perfect Node Tree, with the exception of maybe file=, and perhaps another rndom attribute from old tree format
    # I need to start attempting to port this into the ricecooker, wrapping the old method to work with my new method
    #
