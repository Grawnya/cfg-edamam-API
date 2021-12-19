from tkinter import *
from PIL import Image, ImageTk
import requests
import re

root = Tk()
root.title('Recipe Search')
p1 = PhotoImage(file = 'broccoli 32x32.png')
root.iconphoto(False, p1)
root.geometry('640x600')
root.configure(bg = 'white')

def specific_recipe(dict_of_recipes):
	global recipe_name, more_details
	recipe_name = read_in_recipe.get()
	recipe_name = recipe_name.lower() # format to lower case and then use 'title' to capitalise each word to format the section headings
	recipe_name = recipe_name.title()
	# value = list(dict_of_recipes.keys().index(recipe_name))
	code = dict_of_recipes[recipe_name]#.values()[value[0]]
	app_id = 'ca261162'
	app_key = '8db2cb0cfee4703dc5b1f2520808fbae'
	result = requests.get(
		f'https://api.edamam.com/api/recipes/v2/{code}?type=public&app_id={app_id}&app_key={app_key}'
	)
	data = result.json()
	more_details = data['recipe']

	lines = []
	lines.append(f'{recipe_name}')

	# print cuisine type
	format_in_gui(lines, more_details, 'cuisineType')

	# print meal type
	format_in_gui(lines, more_details, 'mealType')

	# print total time
	format_in_gui(lines, more_details, 'totalTime')

	# print calories
	format_in_gui(lines, more_details, 'calories')

	# print ingredients
	format_in_gui(lines, more_details, 'ingredientLines', True)

	# print health details  
	format_in_gui(lines, more_details, 'healthLabels')

	# print diet details  
	format_in_gui(lines, more_details, 'dietLabels')

	specific = Tk()
	specific.title(f'{lines[0]}')
	specific.configure(bg = 'white')

	specific_recipe_label = Label(specific, text=f'{lines[0]}')
	specific_recipe_label.grid(row=0, column=0)
	specific_recipe_label.configure(background='white', font=('Arial', 12, 'bold'), foreground='black')

	j = 1
	while j < len(lines):
		while j < len(lines):
			specific_recipe_label = Label(specific, text=f'{lines[j]}')
			specific_recipe_label.grid(row=j, sticky='w')
			specific_recipe_label.configure(background='white', font=('Arial', 10), foreground='black')
			j += 1
	
	specific.mainloop()

def format_in_gui(lines_to_print, list_of_details, specific_item, sort=False):
	if sort == True:
		list_of_elements = sorted(list_of_details[specific_item])
	elif sort == False:
		list_of_elements = list_of_details[specific_item]
	name = re.split('(?=[A-Z])', specific_item)
	label = ' '.join(name)
	title = label[0].upper() + label[1:]
	lines_to_print.append(f'{title}:')
	i = 0
	if type(list_of_elements) == float:
		new_element = f'{list_of_elements:.2f}'
		lines_to_print.append(new_element)
	else: 
		while i < len(list_of_elements)/4 + 1:
			lst = list_of_elements[4*i:4*(i+1)]
			ingre = ', '.join(lst)
			lines_to_print.append(ingre)
			i += 1

def read_vals():
	ingredients = ingredient_text.get()
	diet = diet_menu.get()
	cuisine = cuisine_menu.get()
	meal = var.get()
	meal = meal.lower()
	health = health_menu.get()
	min_time = min_time_text.get()
	max_time = max_time_text.get()
	min_cals = min_calories_text.get()
	max_cals = max_calories_text.get()
	exclude = exclude_text.get()
	global recipe_list
	recipe_list = run_api(ingredients, diet, cuisine, meal, health, min_time, max_time, min_cals, max_cals, exclude)
	specific_gui(recipe_list)
	return recipe_list

def run_api(ingredients, diet, cuisine, meal, health, min_time, max_time, min_cals, max_cals, exclude):
	app_id = 'ca261162'
	app_key = '8db2cb0cfee4703dc5b1f2520808fbae'
	link = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredients}&app_id={app_id}&app_key={app_key}'
	if min_time != '' and max_time != '' and min_time.isdigit() == True and max_time.isdigit() == True:
		link += f'&time={min_time}-{max_time}'
	if diet != 'None' and diet != 'DASH':
		diet = diet.lower()
		link += f'&diet={diet}'
	elif diet == 'DASH':
		link += f'&diet={diet}'
	if cuisine != 'None':
		link += f'&cuisineType={cuisine}'
	if meal != '':
		link += f'&mealType={meal}'
	if health != 'None':
		health = health.lower()
		link += f'&health={health}'
	if min_cals != ('' or 'Min') and max_cals != (''or 'Max') and min_cals.isdigit() == True and max_cals.isdigit() == True:
		link += f'&calories={min_cals}-{max_cals}'
	if exclude != '':
		link += f'&excluded={exclude}'
	result = requests.get(link)
	data = result.json() # returns in JSON format
	list_of_results = data['hits']
	return list_of_results
	
def specific_gui(list_of_recipes):
	global details, read_in_recipe
	details = {} # blank dictionary to populate with the name of the recipe and its specific id

	for result in list_of_recipes:
		recipe = result['recipe']
		name = recipe['label']
		unique_link = recipe['uri'].split('_')[1] # remove the id from the link
		details[name] = unique_link # set the dictionary key and the value it equals

	mini = Tk()
	mini.title('Recipe Titles')
	mini.configure(bg = 'white')

	name_of_recipe = list(details.keys())
	codes = list(details.values())
	i = 1

	title_question = Label(mini, text='Recipe Options')
	title_question.grid(row=i-1, column=0, pady=(10, 5))
	title_question.configure(background='white', font=('Arial', 12, 'bold'), foreground='black')

	while i <= len(name_of_recipe):
		specific_recipe_label1 = Label(mini, text=f'{i}. {name_of_recipe[i-1]}\t')
		specific_recipe_label1.grid(row=i, column= 0, padx=20, pady=5, sticky='W')
		specific_recipe_label1.configure(background='white', font=('Arial', 11), foreground='black')

		specific_recipe_label2 = Label(mini, text=f'{i+1}. {name_of_recipe[i]}')
		specific_recipe_label2.grid(row=i, column= 1, padx=20, pady=5, sticky='W')
		specific_recipe_label2.configure(background='white', font=('Arial', 11), foreground='black')
		i += 2

	# specific recipe
	ask_for_recipe = Label(mini, text='What recipe would you like to see: ')
	ask_for_recipe.grid(row=i-1, column=0, pady=(10, 5), padx=(20, 5), sticky='W')
	ask_for_recipe.configure(bg='white', font=('Arial', 11))
	
	read_in_recipe = Entry(mini, width=68, highlightbackground='black', highlightthickness=2)
	read_in_recipe.grid(row=i-1, column=1, columnspan=3, pady=(10, 5), padx=(5, 20), sticky='W')

	edit_search = Button(mini, text=f'Edit Search', width=10, height=2, relief='raised', borderwidth=2, command=mini.destroy)
	edit_search.grid(row=i, column=1, pady=(10, 20), padx=10)
	edit_search.configure(background='#C6D9B9', font=('Arial', 11), foreground='black')
	
	confirm_search = Button(mini, text=f'Specific Recipe', width=15, height=2, relief='raised', borderwidth=2, command=lambda: specific_recipe(details))
	confirm_search.grid(row=i, column=2, pady=(10, 20), padx=10)
	confirm_search.configure(background='#C6D9B9', font=('Arial', 11), foreground='black')

	mini.mainloop()

# logo row 0 middle of 3 columns
image = Image.open('Main Image.png')
resized_image = image.resize((300,200), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)
start_image = Label(root, image=new_image)
start_image.grid(row=0, column=0, columnspan=4)
start_image.configure(background='white')

# ingredient search row 1
ingredient_label = Label(root, text='Ingredient(s):')
ingredient_label.grid(row=1, column=0, pady=(10, 5), padx=(20, 5), sticky='W')
ingredient_label.configure(bg='white', font=('Arial', 11))

ingredient_text = Entry(root, width=68, highlightbackground='black', highlightthickness=2)
ingredient_text.grid(row=1, column=1, columnspan=3, pady=(10, 5), padx=(5, 20), sticky='W')

# diet drop down in row 2, columns 0 and 1
diet_label = Label(root, text='Diet Label:')
diet_label.grid(row=2, column=0, pady=5, padx=(20,5), sticky='W')
diet_label.configure(bg='white', font=('Arial', 11))

diet_menu = StringVar(root)
diet_menu.set('None') # default value
diet_drop_down = OptionMenu(root, diet_menu, 'None', 'Balanced', 'High-Fiber', 'High-Protein', 'Low-Carb', 'Low-Fat', 'Low-Sodium')
diet_drop_down.configure(width=10, bg='#C6D9B9', anchor= 'center', font=('Arial', 11), foreground='black')
diet_drop_down.grid(row=2, column=1, sticky='w', pady=5, padx=(5, 10))

# cuisine drop down row 2, columns 2 and 3
cuisine_label = Label(root, text='Cuisine Type:')
cuisine_label.grid(row=2, column=2, pady=5, padx=(10,5), sticky='W')
cuisine_label.configure(bg='white', font=('Arial', 11))

cuisine_menu = StringVar(root)
cuisine_menu.set('None') # default value
cuisine_drop_down = OptionMenu(root, cuisine_menu, 'None', 'American', 'Asian', 'British', 'Caribbean', 'Central Europe', 'Chinese', 'Eastern Europe', 'French', 'Indian', 'Italian', 'Japanese', 'Kosher', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'South American', 'South East Asian')
cuisine_drop_down.configure(width=15, bg='#C6D9B9', anchor= 'center', font=('Arial', 11), foreground='black')
cuisine_drop_down.grid(row=2, column=3, sticky='w', pady=5, padx=(5, 20))

# meal type radio button rows 3-7 breakfast, lunch, dinner, snack, teatime
meal_label = Label(root, text='Meal Type:')
meal_label.grid(row=3, column=0, pady=5, padx=(20,5), sticky='W')
meal_label.configure(bg='white', font=('Arial', 11))

var = StringVar(root)
option1 = Radiobutton(root, text='Breakfast', tristatevalue = 0, variable=var, value='Breakfast')
option1.deselect()
option1.grid(row=3, column=1, sticky='w', pady=5, padx=(5, 10))
option1.configure(bg='white', font=('Arial', 11))

option2 = Radiobutton(root, text='Lunch', tristatevalue = 0, variable=var, value='Lunch')
option2.deselect()
option2.grid(row=4, column=1, sticky='w', pady=5, padx=(5, 10))
option2.configure(bg='white', font=('Arial', 11))

option3 = Radiobutton(root, text='Dinner', tristatevalue = 0, variable=var, value='Dinner')
option3.deselect()
option3.grid(row=5, column=1, sticky='w', pady=5, padx=(5, 10))
option3.configure(bg='white', font=('Arial', 11))

option4 = Radiobutton(root, text='Snack', tristatevalue = 0, variable=var, value='Snack')
option4.deselect()
option4.grid(row=6, column=1, sticky='w', pady=5, padx=(5, 10))
option4.configure(bg='white', font=('Arial', 11))

option5 = Radiobutton(root, text='Teatime', tristatevalue = 0, variable=var, value='Teatime')
option5.deselect()
option5.grid(row=7, column=1, sticky='w', pady=5, padx=(5, 10))
option5.configure(bg='white', font=('Arial', 11))

# health type dropdown row 3
health_label = Label(root, text='Health Label:')
health_label.grid(row=3, column=2, pady=5, padx=(10,5), sticky='W')
health_label.configure(bg='white', font=('Arial', 11))

health_menu = StringVar(root)
health_menu.set('None') # default value
health_drop_down = OptionMenu(root, health_menu, 'None', 'Kosher', 'Vegan', 'Vegetarian', 'Shellfish-Free', 'Peanut-Free')
health_drop_down.configure(width=15, bg='#C6D9B9', anchor= 'center', font=('Arial', 11), foreground='black')
health_drop_down.grid(row=3, column=3, sticky='w', pady=5, padx=(5, 20))

# calories min and max row 4 and row 5
calories_label = Label(root, text='Calories(s):')
calories_label.grid(row=4, column=2, pady=5, padx=(10, 5), sticky='W')
calories_label.configure(bg='white', font=('Arial', 11))

min_calories_text = Entry(root, width=26, highlightbackground='black', highlightthickness=2)
min_calories_text.grid(row=4, column=3, columnspan=3, pady=5, padx=(5, 20), sticky='W')
min_calories_text.insert(END, 'Min')

max_calories_text = Entry(root, width=26, highlightbackground='black', highlightthickness=2)
max_calories_text.grid(row=5, column=3, columnspan=3, pady=5, padx=(5, 20), sticky='W')
max_calories_text.insert(END, 'Max')

# time and max row 6 and row 7
time_label = Label(root, text='Time:')
time_label.grid(row=6, column=2, pady=5, padx=(10, 5), sticky='W')
time_label.configure(bg='white', font=('Arial', 11))

minutes_label = Label(root, text='(Minutes)')
minutes_label.grid(row=7, column=2, pady=5, padx=(10, 5), sticky='W')
minutes_label.configure(bg='white', font=('Arial', 11))

min_time_text = Entry(root, width=26, highlightbackground='black', highlightthickness=2)
min_time_text.grid(row=6, column=3, columnspan=3, pady=5, padx=(5, 20), sticky='W')
min_time_text.insert(END, 'Min')

max_time_text = Entry(root, width=26, highlightbackground='black', highlightthickness=2)
max_time_text.grid(row=7, column=3, columnspan=3, pady=5, padx=(5, 20), sticky='W')
max_time_text.insert(END, 'Max')

# ingredient excluded due to allergy row 8
exclude_label = Label(root, text='Exclude/Allergy Food(s):')
exclude_label.grid(row=8, column=0, pady=5, padx=(20, 5), sticky='W')
exclude_label.configure(bg='white', font=('Arial', 11))

exclude_text = Entry(root, width=68, highlightbackground='black', highlightthickness=2)
exclude_text.grid(row=8, column=1, columnspan=3, pady=5, padx=(5, 20), sticky='W')

# search button row 9
search = Button(root, text='Search', width=10, height=2, relief='raised', borderwidth=2, command=read_vals)
search.grid(row=9, column=1, columnspan=2, pady=(10, 20))
search.configure(background='#C6D9B9', font=('Arial', 11), foreground='black')

root.mainloop()