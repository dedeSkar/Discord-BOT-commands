import discord, math, asyncio, random, requests, json, time, asyncio, io, aiohttp
from discord.ext import commands

#those 2 functions are used for todo commands
#file save command
def file_save(member):
    global todo_items
    text_documment = open('./data/' + str(member) + '_to_do_list.txt', 'w+')
    for i in range(0, len(todo_items)):
        text_documment.write(todo_items[i] + '\n')
    text_documment.close()

#function used for opening text files
def file_open(member):
    global todo_items
    todo_items=[]
    with open('./data/' + str(member) + '_to_do_list.txt') as file:
        todo_items = [line.rstrip() for line in file] 

class discord_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online')
    
    #Quick Note, this remind command will not work if the program was restarted
    @commands.command() #Reminds user about the text that he wrote 
    async def remind(self, ctx, user_seconds, *, user_remind_text):
    #check what end does string have, to set time acordingly
        time_provided = user_seconds
        if user_seconds.endswith('h'): #some pajeet code right there
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60
        elif user_seconds.endswith('min'):
            user_seconds = user_seconds[:-3] 
            user_seconds = int(user_seconds) * 60
        elif user_seconds.endswith('s'):
            user_seconds = user_seconds[:-1]
        elif user_seconds.endswith('d'):
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60 * 24
        elif user_seconds.endswith('w'):
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60 * 24 * 7 
    #checks if it's positive, if all is good it will start the timer
        if int(user_seconds) > 0:
            print(f'{ctx.message.author.name} has used remind_me function, it will last for {user_seconds} seconds')
            await ctx.send(f'You will be reminded of *{user_remind_text}* in **{time_provided}**')
            await asyncio.sleep(int(user_seconds))
            await ctx.send(f'<@{ctx.message.author.id}> I remind you that: {user_remind_text}')
            print(f'{ctx.message.author.name} has been reminded of {user_remind_text}')
        elif user_seconds == 0: #checks if user seconds are equal to 0
            await ctx.send(f"<@{ctx.message.author.id}>, dont choose 0")
            print(f'{ctx.message.author.name} provided wrong information for the function remind_me')
        else:
            await ctx.send('Choose a postive integer')
            print(f'{ctx.message.author.name} provided wrong information for the function remind_me')

#the following commands are all part of todo_list
#for the todo to work you need to have folder /data/ in the same directory as your main .py file
#This could be improved, because right now it saves data in .txt file
    #open user's todo list, if it doesnt exist it creates one
    @commands.command()
    async def todo_list(self, ctx):
        member = ctx.message.author.id
        try:
            file_open(member)
            message = ['Here is your to do list:']
            for i in range(0, len(todo_items)):
                message.append(f"{i+1}. {todo_items[i]}")
            await ctx.send("\n".join(message)) 
            member = ctx.message.author.name
            print(f'{member} opened his list')
        
        except FileNotFoundError:
            text_documment = open('./data/' + str(member) + '_to_do_list.txt', 'w+')
            text_documment.close()
            await ctx.send('Your personal list was created')
            member = ctx.message.author.name
            print(f'{member} created a new txt file')

    #adds new tasks to the user's todo list
    @commands.command()
    async def todo_add(self, ctx, *, new_task):
        try:
            member = ctx.message.author.id
            file_open(member)
            todo_items.append(new_task)
            file_save(member)
            await ctx.send('New task was added to your to do list')
            member = ctx.message.author.name
            print(f'{member} added new task to his list')
        except FileNotFoundError:
            text_documment = open('./data/' + str(member) + '_to_do_list.txt', 'w+')
            text_documment.close()
            await ctx.send('Your personal list was created')
            member = ctx.message.author.name
            print(f'{member} created a new txt file')
            member = ctx.message.author.id
            file_open(member)
            todo_items.append(new_task)
            file_save(member)
            await ctx.send('New task was added to your to do list')
            member = ctx.message.author.name
            print(f'{member} added new task to his list')

    #To delete tasks from todo list
    @commands.command()
    async def todo_del(self, ctx, task_remove):
        member = ctx.message.author.id
        file_open(member)
        del todo_items[int(task_remove) - 1]
        file_save(member)
        await ctx.send('Task was deleted, from to do list')
        member = ctx.message.author.name
        print(f'{member} added delete task of his list')

    #this command is used for sorting the list by ABC 
    @commands.command()
    async def todo_sort(self, ctx):
        member = ctx.message.author.id
        file_open(member)
        todo_items.sort(key=str.lower)
        file_save(member)
        await ctx.send('To do list was sorted by ABC')
        member = ctx.message.author.name
        print(f'{member} sorted out his list by ABC')
    
    #With this command user can clear his todo list
    @commands.command()
    async def todo_clear(self, ctx):
        member = ctx.message.author.id
        text_documment = open('./data/' + str(member) + '_to_do_list.txt', 'w+')
        text_documment.close()
        await ctx.send('To do list was cleared')
        member = ctx.message.author.name
        print(f'{member} cleared his list')
# ^^^ The last one todo command
    #Command that outputs the weather of city that user has requested
    @commands.command()
    async def weather(self,ctx, *,  user_city):
        main_text = []      #You need to enter your own api key right here, for this to work
        api_key = 'api_key' #You can get it by registering in openweathermap.org
        user_city = user_city.lower()
        r = requests.get(f' http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={api_key}') #Dont be like me, dont do this
        member, status = ctx.message.author.name, r.status_code                                            #This is bad way of doing request
        print(f'{member} requested weather information about {user_city}, status code: {status}')
        weather_data = r.json()
        if status != 200:
            await ctx.send('That city does not exist') 
        else:
            user_city = user_city.title()
            weather_main, weather_desc, weather_temp = weather_data["weather"][0]["main"], weather_data["weather"][0]["description"], weather_data["main"]['temp']
            weather_wind, weather_country = weather_data['wind']['speed'], weather_data['sys']['country']   
            main_text.append(f'__{user_city} weather information:__')
            main_text.append(f'**Weather:** {weather_main}')
            main_text.append(f'**Weather description:** {weather_desc.title()}')
            main_text.append(f'**Temperature:** {round(weather_temp - 273.15, 2)}°C')
            main_text.append(f'**Wind speed:** {weather_wind}m/s')
            main_text.append(f'**Country:** {weather_country} :flag_{weather_country.lower()}:')
            await ctx.send("\n".join(main_text))

    #Basically user can request a random joke from the internet 
    @commands.command()
    async def joke(self, ctx):
        r = requests.get('https://sv443.net/jokeapi/v2/joke/Any')
        status = r.status_code
        print(f'{ctx.message.author.name} has requested a joke, status = {status}')
        joke_data = r.json()
        joke_type = joke_data["type"]
        if joke_type == 'twopart': #Basically this let's me know what kind of type of joke this is
            joke_setup, joke_delivery = joke_data["setup"], joke_data["delivery"]
            await ctx.send(joke_setup + '\n' + joke_delivery)
        else:
            await ctx.send(joke_data['joke'])

    #Function that gets information about X topic from duckduckgo
    @commands.command()
    async def info(self, ctx, *, user_question):
        r = requests.get(f'https://api.duckduckgo.com/?q={user_question}&format=json')
        print(f'{ctx.message.author.name} has asked a question on duckduckgo about {user_question}, status = {r.status_code}')
        if r.status_code == 200:
            answer_data = r.json()
            try:
                if answer_data['AbstractText'] != '': #It prioritizes the text from wikipedia
                    answer_source = answer_data['AbstractSource']
                    answer_text = answer_data["AbstractText"]
                    await ctx.send(f'**Answer: **{answer_text}\n**Source: **{answer_source}')
                elif answer_data["Definition"] !='':
                    answer_text = answer_text["Definition"]
                    answer_source = answer_text["DefinitionSource"]
                    await ctx.send(f'**Answer: **{answer_text}\n**Source: **{answer_source}')
                elif answer_data["RelatedTopics"][0]["Text"] != '':
                    answer_text = answer_data["RelatedTopics"][0]["Text"]
                    await ctx.send(f'**Answer: **{answer_text}')
                if answer_data["Image"] != '':
                    url = answer_data["Image"]
                    async with aiohttp.ClientSession() as session:  
                        async with session.get(url) as resp:
                            if resp.status != 200:
                                return print(f'Could not download file...from {url}')
                            data = io.BytesIO(await resp.read())
                    await ctx.send(file=discord.File(data, 'reference.png'))
            except: #This is some shitty pajeet spagheti code, but I dont care at this point, it was suppost to be temp fix
                i = 0
                list_len = 0
                related_answer_main_text = []
                while True: #Till it's not IndexError it will keep searching for related stuff
                    try:
                        answer_related = answer_data["RelatedTopics"][0]["Topics"][i]['FirstURL']
                        related_url, related_word = answer_related.split('.com/')
                        related_url = related_url.title #only done this so that vscode would stop bitching
                        if '%' not in related_word:
                            related_word = related_word.replace('_', ' ')
                            related_word = related_word.replace('d/', '')
                            list_len += 1
                            related_answer_main_text.append(f'{list_len}. {related_word}')
                        i += 1
                    except IndexError:
                        break
                if related_answer_main_text != []:
                    related_answer_main_text.insert(0, f"I dont have information about {user_question}, but I do have information about:")
                    await ctx.send("\n".join(related_answer_main_text))
                else:
                    await ctx.send(f'I dont have information about {user_question}')    
        else: #If status code is not 200 it prints out this
            await ctx.send(f'Something went wrong....')
    
    #outputs image to dc server chat
    @commands.command()
    async def img(self, ctx, *, user_photo_request):
        user_photo_request = user_photo_request.replace(' ', ',')
        async with aiohttp.ClientSession() as session:          #You \/ can change resulotion right here
            async with session.get('https://source.unsplash.com/1920x1080/?' + user_photo_request) as resp: 
                if resp.status != 200:
                    return print(f'Could not download file...from unsplash/{user_photo_request}')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'photo.png'))
                print(f'{ctx.message.author.name} has requested photo from Unsplash - {user_photo_request}')

    #finds definiotion of the word in the urban dictionary
    @commands.command()
    async def urband(self, ctx, *, user_request_word):
        user_request_word = user_request_word.lower()
        host = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":f"{user_request_word}"}
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': "api_key" #for this to work you need to get your own api key
            }                           #from x_rapidapi
        response = requests.request("GET", host, headers=headers, params=querystring)
        print(f'{ctx.message.author.name} has requested information from Urban Dictionary about {user_request_word}, status: {response.status_code}')
        try:
            if response.status_code == 200: #basically to check if everything is alright    
                urban_data = response.json()
                message = urban_data["list"][0]["definition"]
                message = message.replace('[', '')
                await ctx.send(f"**{user_request_word.title()}** is {message.replace(']', '')}")
            else:
                await ctx.send(f"I couldnt find definition of {user_request_word}")
        except IndexError:
            await ctx.send(f"I couldnt find definition of {user_request_word}")
    
    #outputs random quote
    @commands.command()
    async def quote(self, ctx):
        main_text = []
        host = 'https://quotes.rest/qod?category=inspire'
        api_key = "api_key" #You need to get your own api key, from that site
        headers = {'content-type': 'application/json',
            'X-TheySaidSo-Api-Secret': format(api_key)}
        response = requests.get(host, headers=headers)
        print(f'{ctx.message.author.name} has requested a quote, status = {response.status_code}')
        if response.status_code == 200:
            quotes=response.json()['contents']['quotes'][0]["quote"]
            main_text.append(quotes)
            author = response.json()['contents']['quotes'][0]["author"]
            main_text.append(f'**Author: **{author}')
            await ctx.send("\n".join(main_text))
        elif response.status_code == 429: 
            await ctx.send('Hourly quote limit has been reached')
        else:
            await ctx.send('Something went wrong.... ')

    #sends a webm when asked, from local collection
    #For this to work you need to have folder named /webms/ in the same directory as main .py file
    #and all webms should be named from 1 to X number
    @commands.command()
    async def webm(self, ctx):
        print(f'{ctx.message.author.name} has requested webm from')
        webm_number = random.randint(1, 84)
        await ctx.send(file=discord.File('./webms/' + str(webm_number) + '.webm'))
    
def setup(client):
    client.add_cog(discord_commands(client))
