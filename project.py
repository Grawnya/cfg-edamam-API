import requests
import re

# function to access the API with basic criteria
def basic_recipe_search(ingredient):  
    app_id = 'ca261162'
    app_key = '8db2cb0cfee4703dc5b1f2520808fbae'
    time = input('Desired cooking time range in minutes in form (min)-(max): ')
    result = requests.get( # extended link commented out whichc includes other important search criteria - can be added by strin concatenation if box filled in GUI
        f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}'#&diet=low-sodium&cuisineType=Italian&mealType=Lunch&calories=200-400&time={time}&excluded=chocolate&random=false&nutrients%5BENERC_KCAL%5D=500-700'
    )
    data = result.json() # returns in JSON format
    return data['hits'] # obtain list of all recipes that fit criteria

# function 
def print_item_to_console(list_of_details, specific_item, sort=False):
    if sort == True: # criteria to sort ingredients, without creating a new function - can ignore argument if not sorted
        list_of_elements = sorted(list_of_details[specific_item]) 
    elif sort == False: # default case will not sort list
        list_of_elements = list_of_details[specific_item]
    name = re.split('(?=[A-Z])', specific_item) # split at the capital letter, as names use camel case - into list
    label = ' '.join(name) # join the split names list with a space in between each word
    title = label[0].upper() + label[1:] # capitalise the first letter and ignore the rest - just for formatting
    print(f'\n{title}:') 
    if type(list_of_elements) == float: # calories and time are float items, so are not looped through and are printed individually
        print(f'{list_of_elements:.2f}') # to 2 decimal places as a floating point number(2 types of floats)
    else:
        for each in list_of_elements: # loop through all lists and print each element
            print(each)

# function to format the document - similar to printing to console formatting, but just additional function 
# as both printing to a doc and console don't need to occur
def format_in_document(lines_to_print, list_of_details, specific_item, sort=False):
    if sort == True:
        list_of_elements = sorted(list_of_details[specific_item])
    elif sort == False:
        list_of_elements = list_of_details[specific_item]
    name = re.split('(?=[A-Z])', specific_item)
    label = ' '.join(name)
    title = label[0].upper() + label[1:]
    lines_to_print.append(f'\n{title}:')
    if type(list_of_elements) == float:
        new_element = f'\n{list_of_elements:.2f}'
        lines_to_print.append(new_element)
    else:
        for each in list_of_elements:
            lines_to_print.append(f'\n{each}')
    lines_to_print.append('\n')


# function to get the initial list of the recipes
def run():
    ingredient = input('Enter an ingredient: ') # multiple can actually be entered - with or without commas
    results = basic_recipe_search(ingredient)
    details = {} # blank dictionary to populate with the name of the recipe and its specific id
    for result in results:
        recipe = result['recipe']
        name = recipe['label']
        unique_link = recipe['uri'].split('_')[1] # remove the id from the link
        details[name] = unique_link # set the dictionary key and the value it equals
        print(name) # print name onto console
    return details # return the dictionary

# function to print the specific recipe to console/terminal
def specific_recipe_to_console(dict_of_recipes):
    recipe_name = input('\nWhat recipe is of most interest? ') # read in specific recipe
    recipe_name = recipe_name.lower() # format it by making it lower case and then capitalising each word
    recipe_name = recipe_name.title()
    if recipe_name not in dict_of_recipes: # To catch out any misspelt words
        recipe_name = input('\nName not valid. What recipe is of most interest? ')
        recipe_name = recipe_name.lower()
        recipe_name = recipe_name.title()
    app_id = 'ca261162'
    app_key = '8db2cb0cfee4703dc5b1f2520808fbae'
    code = dict_of_recipes[recipe_name]
    result = requests.get(
        f'https://api.edamam.com/api/recipes/v2/{code}?type=public&app_id={app_id}&app_key={app_key}' # speciifc recipe link
    )
    data = result.json()
    more_details = data['recipe']
    print(f'{recipe_name}\n')

    # print cuisine type
    print_item_to_console(more_details, 'cuisineType')

    # print meal type
    print_item_to_console(more_details, 'mealType')

    # print total time
    print_item_to_console(more_details, 'totalTime')
    print('minutes')

    # print calories
    print_item_to_console(more_details, 'calories')
    print('kcals')

    # print ingredients
    print_item_to_console(more_details, 'ingredientLines', True)

    # print health details  
    print_item_to_console(more_details, 'healthLabels')

    # print diet details  
    print_item_to_console(more_details, 'dietLabels')

# function to write the recipe to a text file - similar explanations to 'specific_recipe_to_console' function above
def write_to_file(dict_of_recipes):
    recipe_name = input('\nWhat recipe is of most interest? ')
    recipe_name = recipe_name.lower()
    recipe_name = recipe_name.title()
    if recipe_name not in dict_of_recipes:
        recipe_name = input('\nName not valid. What recipe is of most interest? ')
        recipe_name = recipe_name.lower()
        recipe_name = recipe_name.title()
    code = dict_of_recipes[recipe_name]
    app_id = 'ca261162'
    app_key = '8db2cb0cfee4703dc5b1f2520808fbae'
    result = requests.get(
        f'https://api.edamam.com/api/recipes/v2/{code}?type=public&app_id={app_id}&app_key={app_key}'
    )
    data = result.json()
    lines = []
    more_details = data['recipe']
    lines.append(f'{recipe_name}\n')

    # print cuisine type
    format_in_document(lines, more_details, 'cuisineType')

    # print meal type
    format_in_document(lines, more_details, 'mealType')

    # print total time
    format_in_document(lines, more_details, 'totalTime')
    lines.append('minutes\n')

    # print calories
    format_in_document(lines, more_details, 'calories')
    lines.append('kcals\n')

    # print ingredients
    format_in_document(lines, more_details, 'ingredientLines', True)

    # print health details  
    format_in_document(lines, more_details, 'healthLabels')

    # print diet details  
    format_in_document(lines, more_details, 'dietLabels')

    # write to a file
    textfile = open('recipe.txt', 'w')
    for element in lines:
        textfile.write(element)
    textfile.close()

# comment out 'specific_recipe_to_console' or 'write_to_file' based on what you want to happen
recipes = run()
specific_recipe_to_console(recipes)
# write_to_file(recipes)