import os


class ConsoleMenu(object):
    options = list()
    currparam = list()

    def __init__(self):
        self.options = []
        self.currparam = []
        self.options.append(ConsoleOption("help", self.printhelp, d="Prints this help menu"))
        self.options.append(ConsoleOption("cm_dir", ConsoleMenu.print_cm, d="Prints all available commands"))
        self.options.append(ConsoleOption("cm_do", self.perform,
                                          d="Prints all available commands. <directory> <type> <com>",
                                          p=["string", "string", "string"]))
        self.options.append(ConsoleOption("cm_t", ConsoleMenu.print_types, d="Prints cm types"))
        self.options.append(ConsoleOption("exit", ConsoleOption.stop, d="Exits current menu"))

    def addcommand(self, command, func, desc="", p=None):
        if p is None:
            p = list()
        option = ConsoleOption(command, func, p, desc)
        self.options.insert(len(self.options)-1, option)

    def getcommand(self, com):
        splits = com.split(" ")
        if len(splits) == 0:
            return ConsoleOption.blank()
        command = splits.pop(0)

        for i in self.options:
            self.currparam.clear()
            if i.command == command:
                # Get all parameters or return 'bad_parameters'

                if len(i.param) > len(splits):
                    continue

                for j in range(len(i.param)):

                    if i.param[j] == "string":
                        self.currparam.append(splits[j])
                    elif i.param[j] == "int":
                        try:
                            self.currparam.append(int(splits[j]))
                        except ValueError as err:
                            return ConsoleOption.bad_parameters
                    elif i.param[j] == "float":
                        try:
                            self.currparam.append(float(splits[j]))
                        except ValueError as err:
                            return ConsoleOption.bad_parameters
                    elif i.param[j] == "complex":
                        try:
                            self.currparam.append(complex(splits[j]))
                        except ValueError as err:
                            return ConsoleOption.bad_parameters
                    elif i.param[j] == "bool":
                        try:
                            self.currparam.append(bool(splits[j]))
                        except ValueError as err:
                            return ConsoleOption.bad_parameters

                # Ensure all parameters have been accounted for
                if len(self.currparam) != len(i.param):
                    return ConsoleOption.bad_parameters

                # Put the rest of the parameters as one string
                rest = ""
                for j in range(len(i.param), len(splits)):
                    rest += splits[j]
                    if j != (len(splits) - 1):
                        rest += " "
                self.currparam.append(rest)
                return i.func

        # Not a command
        return ConsoleOption.blank

    def printhelp(self):
        print("\n -- Help Menu --")
        for i in self.options:
            print(i)
        print()
        return True

    def perform(self):
        # Check if a available file, with right extension
        fi = str(self.currparam[0])
        dirs = ConsoleMenu.get_inputs()
        if not dirs.__contains__(fi):
            print("That is not a command file!")
            return True
        elif not fi.endswith(".cm"):
            print("That is not a valid file extension!")
            return True
        # Get other parameters
        fi_t = self.currparam[1]
        fi_com = self.currparam[2]

        # Read file
        text = ""
        try:
            file = open(fi, 'r')

            text = file.read()

            file.close()
        except IOError:
            print("Something went wrong!")
        liszt = text.split("\n")
        if liszt.pop(0) != "%command%":
            print("That file is not valid!")
            return True

        print("Commands: " + str(liszt))

        # Interpret as parametered command
        if fi_t == "param":
            for i in liszt:
                self.getcommand(str(fi_com) + str(i))()
        # Take as raw command
        else:
            for i in liszt:
                self.getcommand(i)()

        return True

    @staticmethod
    def create_empty():
        cm = ConsoleMenu()
        cm.options.clear()
        return cm

    @staticmethod
    def print_types():
        print("Type: \n- raw\n- - Each line is exactly a command\n- param\n"
              "- - Each line is the parameters to a specific command")
        return True

    @staticmethod
    def get_inputs():
        liszt = [f.name for f in os.scandir() if f.is_file()]
        good = list()
        for i in liszt:
            if not str(i).endswith(".cm"):
                continue
            try:
                reader = os.open(i, os.O_RDONLY)
                contents = os.read(reader, 9)
                os.close(reader)
            except OSError:
                continue
            if contents.startswith(b'%command%'):
                good.append(i)

        return good

    @staticmethod
    def print_cm():
        liszt = ConsoleMenu.get_inputs()
        for i in liszt:
            print(i)
        return True


class ConsoleOption(object):
    func = None
    command = str()
    desc = ""
    param = list()

    def __init__(self, com, f, p=None, d=""):
        if p is None:
            p = list()
        self.command = com
        self.func = f
        self.param = p
        self.desc = d

    @staticmethod
    def blank():
        print("That is not a command!")
        return True

    @staticmethod
    def bad_parameters():
        print("That is not a command!\nInvalid parameters.")
        return True

    @staticmethod
    def stop():
        return False

    def __str__(self):
        coll = self.command
        for i in self.param:
            coll += " <" + i + ">"
        if self.desc != "":
            coll += " -> " + self.desc
        return coll

