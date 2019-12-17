from ConsoleControl import *
import time


def kill():
    print("Killing....")
    time.sleep(1)
    print("\nKilled!")
    return True


# Start of program

menu = ConsoleMenu()
menu.addcommand("kill", kill, "Waits for 1 second")

successes = 0
while menu.getcommand(input())():
    successes += 1

print("\nPress enter to quit....")
input()

# End of program
