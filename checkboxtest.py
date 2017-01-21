from easygui import *

message = "What does she say?"
title = ""
if boolbox(message, title, ["She loves me", "She loves me not"]):
    sendher("Flowers") # This is just a sample function that you might write.
else:
    pass