import keyboard  # using module keyboard
# import time

# stop = False
# def onkeypress(event):
#     global stop
#     if event.name == 'q':
#         stop = True

# # ---------> hook event handler
# keyboard.on_press(onkeypress)
# # --------->

# while True:  # making a loop
#     try:  # used try so that if user pressed other than the given key error will not be shown
#         print("sleeping")
#         time.sleep(5)
#         print("slept")
#         if stop:  # if key 'q' is pressed 
#             print('You Pressed A Key!')
#             break  # finishing the loop
#     except:
#         print("#######")
#         break  # if user pressed a key other than the given key the loop will break


# index dictionary by list of key names

keyboard.is_pressed('Q')