def map_select(map_dict):
    '''Have Player Input the desired Map'''
    try:
        print('Chose one of the following map designs')
        print('')
        for item in map_dict:
            print(item)
        print('')
        player_input = input('Type the name of the level here ')
        print('')
        if player_input in map_dict:
            return map_dict[player_input]
        else:
            # Recursivly call func until player inputs valid level name
            print('Invalid input. Please type a level name...')
            print('')
            return map_select(map_dict)
    except:
        print('Invalid input. Please type a level name...')