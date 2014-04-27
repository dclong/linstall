#!/usr/bin/env python
# encoding: utf-8

import os
__des_dir__ = os.path.join(os.environ["HOME"], ".thunderbird")
__profiles_ini__ = os.path.join(__des_dir__, "profiles.ini")
__src_dir__ = os.path.join(os.environ["common"], "thunderbird")

def links(folder, fext, profiles, default_profile, linkfun):
    """@todo: Docstring for links.

    :profiles: @todo
    :returns: @todo

    """
    import os
    # decide destination profile
    src_dir = os.path.join(__src_dir__, folder)
    files = [f for f in os.listdir(src_dir) if f.endswith(fext)]
#    abooks = ["abook.mab", "history.mab"]
    for f in files:
        src_file = os.path.join(src_dir, f)
        print("\nLinking " + f + " ...")
        ps = choose(profiles, default_profile)
        linkfun(f, ps, src_file)
    #end for
#end def 
def link_filter(msg_filter, profiles, src_filter_file):
    """@todo: Docstring for link_filter.

    :profiles: @todo
    :src_filter_file: @todo
    :returns: @todo

    """
    import os
    for p in profiles:
        p = os.path.join(p[1], "ImapMail")
        accounts = [[d, os.path.join(p, d)] for d in os.listdir(p)]
        accounts = [a for a in accounts if os.path.isdir(a[1])]
        accounts = choose(accounts, None)
        for a in accounts:
            des_filter_file = os.path.join(a[1], "msgFilterRules.dat")
            symlink(src_filter_file, des_filter_file)
        #end for
    #end for
#end def 
def link_template(temp, profiles, src_temp_file):
    import os
    for p in profiles:
        des_temp_file = os.path.join(p[1], "quicktext", "templates.xml")
        symlink(src_temp_file, des_temp_file)
    #end for
#end def
def link_abook(abook, profiles, src_abook_file):
    """@todo: Docstring for link_abook.

    :profiles: @todo
    :abook: @todo
    :returns: @todo

    """
    import os
    for p in profiles:
        des_abook_file = os.path.join(p[1], abook)
        symlink(src_abook_file, des_abook_file)
    #end for
#end def 
def symlink(src, des):
    """@todo: Docstring for symlink.

    :src: @todo
    :des: @todo
    :returns: @todo

    """
    import os
    symlink_command = 'ln -Tsvf "' + src + '" "' + des + '"'  
    os.system(symlink_command)
#end def 
def choose(choices, default=None):
    """@todo: Docstring for choose_profile.

    :profiles: @todo
    :returns: @todo

    """
    import sys
    n = len(choices)
    for i in range(n):
        print(str(i) + ": " + choices[i][0])
    #end for
    msg = "Please choose an index"
    if default == None:
        msg += ":"
    else:
        msg += " (default: " + default[0] + "):"
    #end if
    print(msg)
    print("A/a: all")
    print("F/f: first")
    print("L/l: last")
    print("N/n: none")
    print("C/c: cancel operation")
    choice = raw_input()
    choice = choice.strip().lower()
    if choice == "c":
        sys.exit(0)
    #end if
    if choice == "n":
        return []
    #end if
    if choice == "a":
        return choices
    #end if
    if choice == "f":
        return [choices[0]]
    #end if
    if choice == "l":
        return [choices[-1]]
    #end if
    if default !=None and choice == "":
        return [default_profile]
    #end if
    choice = int(choice)
    return [choices[choice]]
#end def 
def get_profiles():
    """@todo: Docstring for profiles.
    Parses profile.ini to extract all profiles.
    :returns: @todo

    """
    f = open(__profiles_ini__, 'r')
    lines = f.readlines()
    profiles = []
    default_profile = []
    n = len(lines)
    name = None
    relative = None
    path = None
    default = None
    for i in range(n):
        line = lines[i]
        if line.startswith("[Profile"):
            # add profile
            add_profile(profiles, default_profile, name, path, relative, default) 
            # clear variables
            name = None
            path = None
            relative = 1
            default = 0
            continue
        #end if
        if line.startswith("Name="):
            name = line[5:].strip()
            continue
        #end if
        if line.startswith("IsRelative="):
            relative = line[11:].strip()
            continue
        #end if
        if line.startswith("Path="):
            path = line[5:].strip()
            continue
        #end if
        if line.startswith("Default="):
            default = line[8:].strip()
            continue
        #end if
    #end for
    add_profile(profiles, default_profile, name, path, relative, default) 
    return profiles, default_profile
#end def 
def add_profile(profiles, default_profile, name, path, relative, default):
    """@todo: Docstring for add_profile.
    Add a profile into the profiles list.
    :profiles: @todo
    :name: @todo
    :path: @todo
    :relative: @todo
    :returns: @todo

    """
    import os
    if name == None or path == None or relative == None:
        return
    #end if
    if int(relative):
        path = os.path.join(__des_dir__, path)
    #end if
    profiles.append([name, path])
    if int(default):
        default_profile.append(name)
        default_profile.append(path)
    #end if
#end def 
if __name__ == '__main__':
    profiles, default_profile = get_profiles()
    print("\n\nCreating symbolic links for address books ...")
    links("address_books", ".mab", profiles, default_profile, link_abook)
    print("\n\nCreating symbolic links for message filters ...")
    links("message_filters", ".dat", profiles, default_profile, link_filter)
    print("\n\nCreating symbolic links for quicktext templates ...")
    links("quicktext_templates", ".xml", profiles, default_profile, link_template)
#end if
