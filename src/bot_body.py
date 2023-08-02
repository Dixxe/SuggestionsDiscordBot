import disnake
from disnake.ext import commands
import json

################
intents = disnake.Intents.default()
intents.message_content = True

global slash_inter, button_inter

slash_inter: disnake.AppCmdInter
button_inter = disnake.MessageInteraction


activity = disnake.Activity(
    name="Made by dixxe",
    type=disnake.ActivityType.listening)
################
# {u:{[s:[u,d]]}}
suggestions = {} # {'user_nick1' : [{'suggestion1' : [amount_upvotes, amount_downvotes]}, {'suggestion2' : [amount_upvotes, amount_downvotes]}], 'user_nick1' : {'suggestion1' : [amount_upvotes, amount_downvotes]}, {'suggestion2' : [amount_upvotes, amount_downvotes]}}
 # for creation:      suggestions['user_nick1'] = [{'suggestion' : [0, 0]}]
 # for accses it will look like: suggestions['user_nick1'][0]['suggestion1'][0] - get ammount of upvotes for suggestion1
 #                               suggestions['user_nick1'][0]['suggestion1'][1] - get ammount of downvotes for suggestion

 #                               for user in suggestions.keys()
 #                                  for user_suggestion in range(len(suggestions[user]))
#                                        suggestions_dict = suggestions[user][user_suggestion]
#                                        for suggestion in suggestions_dict.keys()
#                                               suggestion_up = suggestions_dict[suggestion][0]
#                                               suggestion_down = suggestions_dict[suggestion][1]
#

##--сохранение--##
def exportData(bufer, warned, bjstats):
    data = {'suggestions': suggestions}
    with open('value.json', 'w') as save:
        json.dump(data, save)
##--сохранение--##

##--загрузка--##
def importData():
    with open('value.json', 'r') as save:
        data = json.load(save)
        suggestions = data['suggestions']
    return suggestions
##--загрузка--##

##--очистка--##
def flushs():
    data = {'suggestions': {}}
    with open('value.json', 'w') as save:
        json.dump(data, save)

bot = commands.Bot(command_prefix='>', intents=intents, help_command=None, activity=activity)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    try: ## проверяю на наличие файлика и обьявляю переменные
        importData()
        global suggestions
        suggestions = importData()
        print(f'Loading succesful. {importData()}')
    except:
        print('No saves found')

@bot.slash_command(description='Все описание всех функций бота.')
async def help(slash_inter):
    await slash_inter.response.defer()
    emb = disnake.Embed(title='Все команды бота:', color=16753920)
    emb.add_field(name='/suggest [предложение]', value='Выскажите ваши мысли')
    emb.add_field(name='/set [текстовый канал]', value='Привязать канал где будет сбор предложений.', inline=False)
    emb.add_field(name='/upvote [эмодзи]', value='Привязать эмодзи отвечающий за положительную реакцию', inline=False)
    emb.add_field(name='/downvote [эмодзи]', value='Привязать эмодзи отвечающий за отрицательную реакцию', inline=False)
    emb.add_field(name='/suggestions', value='Показать все предложения от пользователей.', inline=False)
    emb.set_author(name='Телеграм канал создателя', url='https://t.me/+ok3zStfHZsdjMTQy')
    await slash_inter.edit_original_response(embed=emb)

@bot.slash_command(description='Выскажите ваши мысли')
async def suggest(slash_inter, suggestion : str):
    await slash_inter.response.defer()
    if slash_inter.author.nick in suggestions:
        list = suggestions[slash_inter.author.nick]
        list.append({suggestion : [0, 0]})
    else:
        suggestions[slash_inter.author.name] = [{suggestion : [0, 0]}]
    print(suggestions)

with open('token.txt', 'r') as file:
    token = file.read()

bot.run(token)