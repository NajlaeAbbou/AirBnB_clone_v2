#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import re
import os
from datetime import datetime
import uuid


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''


        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  
            pline = line[:] 

            _cls = pline[:pline.find('.')]

            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """exit the program"""
        exit()

    def help_quit(self):
        """Help for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """exit the program"""
        print()
        exit()

    def help_EOF(self):
        """ help eof """
        print("Exits the program without formatting\n")

    def emptyline(self):
         """empty line + ENTER"""
         pass

    def do_create(self, args):
        """Create  new class inst,print its id"""
        if not args:
            print("** class name missing **")
            return
        list = args.split()
        if list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        mycl = HBNBCommand.classes[list[0]]()
        for arg in list[1:]:
            pr = arg.split('=')
            k = pr[0]
            v = pr[1]
            if v[0] == '\"':
                v = v.replace('\"', '').replace('_', ' ')
            elif '.' in v:
                v = float(v)
            else:
                v = int(v)
            setattr(mycl, k, v)
        mycl.save()
        print(mycl.id)

    def help_create(self):
        """ Help create """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Prints string repres ofan inst based on class name and id"""
        prt = args.partition(" ")
        cl_nom = prt[0]
        cl_id = prt[2]
        if cl_id and ' ' in cl_id:
            cl_id = cl_id.partition(' ')[0]

        if not cl_nom:
            print("** class name missing **")
            return

        if cl_nom not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cl_id:
            print("** instance id missing **")
            return

        k = cl_nom + "." + cl_id
        try:
            print(storage._FileStorage__objects[k])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help show """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Deletes an inst using class name and id"""
        prt = args.partition(" ")
        cl_nom = prt[0]
        cl_id = prt[2]
        if cl_id and ' ' in cl_id:
            cl_id = cl_id.partition(' ')[0]

        if not cl_nom:
            print("** class name missing **")
            return

        if cl_nom not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cl_id:
            print("** instance id missing **")
            return

        k = cl_nom + "." + cl_id

        try:
            del(storage.all()[k])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help destroy"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Prints all string repr of all inst"""
        ob = []

        if args:
            args = args.split(' ')[0]
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(args).items():
                if k.split('.')[0] == args:
                    ob.append(str(v))
        else:
            for k, v in storage.all().items():
                ob.append(str(v))

        print(ob)

    def help_all(self):
        """ Help all"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """number of instances"""
        c = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                c += 1
        print(c)

    def help_count(self):
        """ help count """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates an inst based on class name,id"""
        cl_nom = cl_id = a_nom = av = kwargs = ''
        args = args.partition(" ")
        if args[0]:
            cl_nom = args[0]
        else:
            print("** class name missing **")
            return
        if cl_nom not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        args = args[2].partition(" ")
        if args[0]:
            cl_id = args[0]
        else:
            print("** instance id missing **")
            return
        k = cl_nom + "." + cl_id
        if k not in storage.all():
            print("** no instance found **")
            return
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                a_nom = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')
            if not a_nom and args[0] != ' ':
                a_nom = args[0]
            if args[2] and args[2][0] == '\"':
                av = args[2][1:args[2].find('\"', 1)]
            if not av and args[2]:
                av = args[2].partition(' ')[0]

            args = [a_nom, av]
        nd = storage.all()[k]
        for i, a_nom in enumerate(args):
            if (i % 2 == 0):
                av = args[i + 1]
                if not a_nom:
                    print("** attribute name missing **")
                    return
                if not av:
                    print("** value missing **")
                    return
                if a_nom in HBNBCommand.types:
                    av = HBNBCommand.types[a_nom](av)
                nd.__dict__.update({a_nom: av})

        nd.save()

    def help_update(self):
        """ Help update """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
