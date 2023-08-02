import disnake
from disnake.ext import commands, tasks
from asyncio import sleep
import json
from random import randint

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
global service, suggestions
service = ['⬆️', '⬇️', 123] # [0] - upvote emoji, [1] - downvote emoji, [2] - linked channel id

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
def exportData(suggestions, service):
    data = {'suggestions': suggestions,
            'service'    : service    }
    with open('value.json', 'w') as save:
        json.dump(data, save)
##--сохранение--##

##--загрузка--##
def importData():
    with open('value.json', 'r') as save:
        data = json.load(save)
        suggestions = data['suggestions']
        service = data['service']
    return suggestions, service
##--загрузка--##

##--очистка--##
def flushs():
    data = {'suggestions': {},
            'service': ['⬆️', '⬇️', 123]}
    with open('value.json', 'w') as save:
        json.dump(data, save)

bot = commands.Bot(command_prefix='>', intents=intents, help_command=None, activity=activity)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    check.start()
    try: ## проверяю на наличие файлика и обьявляю переменные
        importData()
        global suggestions, service
        suggestions, service = importData()
        print(f'Loading succesful. {importData()}')
        save.start()
    except:
        print('No saves found')
        save.start()

@bot.slash_command(description='Все описание всех функций бота.')
async def help(slash_inter):
    await slash_inter.response.defer()
    emb = disnake.Embed(title='Все команды бота:', color=16753920)
    emb.add_field(name='>suggest [предложение]', value='Выскажите ваши мысли')
    emb.add_field(name='/upvote [эмодзи]', value='Привязать эмодзи отвечающий за положительную реакцию', inline=False)
    emb.add_field(name='/downvote [эмодзи]', value='Привязать эмодзи отвечающий за отрицательную реакцию', inline=False)
    emb.add_field(name='/set [канал]', value='Привязанный канал где будут предложения.')
    emb.add_field(name='/suggestions', value='Показать все предложения от пользователей.', inline=False)
    emb.set_author(name='Телеграм канал создателя', url='https://t.me/+ok3zStfHZsdjMTQy')
    await slash_inter.edit_original_response(embed=emb)

@bot.command()
async def suggest(ctx):
    if (ctx.channel.id == service[2]):
        if (ctx.author.name in suggestions):
            list = suggestions[ctx.author.name]
            list.append({ctx.message.id : [0, 0]})
        else:
            suggestions[ctx.author.name] = [{ctx.message.id : [0, 0]}]
        try:
            await ctx.message.add_reaction(service[0])
            await ctx.message.add_reaction(service[1])
        except Exception:
            try: 
                upvote = bot.get_emoji(service[0])
                await ctx.message.add_reaction(upvote)
            except Exception: pass
            try: 
                downvote = bot.get_emoji(service[1])
                await ctx.message.add_reaction(downvote)
            except Exception:pass
            
    else:
        await ctx.message.delete()

@bot.slash_command(description='Привязать эмодзи отвечающий за положительную реакцию')
async def upvote(slash_inter, emoji):
    await slash_inter.response.defer(ephemeral=True)
    try: service[0] = emoji.id
    except Exception: pass
    service[0] = emoji
    await slash_inter.edit_original_response(f'Эмодзи {emoji}, привязан как положительная реакция')


@bot.slash_command(description='Привязать эмодзи отвечающий за отрицательную реакцию')
async def downvote(slash_inter, emoji):
    await slash_inter.response.defer(ephemeral=True)
    try: service[1] = emoji.id
    except Exception: pass
    service[1] = emoji
    await slash_inter.edit_original_response(f'Эмодзи {emoji}, привязан как отрицательная реакция')


@bot.slash_command(description='Привязанный канал где будут предложения.')
async def set(slash_inter, channel : disnake.TextChannel):
    await slash_inter.response.defer(ephemeral=True)
    service[2] = channel.id
    await slash_inter.edit_original_response(f"Канал {channel.name} привязан.")
    await announce(service[2])

@bot.slash_command(description='Показать все предложения от пользователей.')
async def suggested(slash_inter):
    await slash_inter.response.defer()
    pair = []
    emb = disnake.Embed(title='Топ предложений:', color=randint(1, 16777216))
    emb.set_author(name='Телеграм канал создателя', url='https://t.me/+ok3zStfHZsdjMTQy')
    for user in suggestions.keys():
        for user_suggestion in range(len(suggestions[user])):
            suggestions_dict = suggestions[user][user_suggestion]
            for suggestion in suggestions_dict.keys():
                msg = bot.get_message(suggestion)
                upvotes = suggestions_dict[suggestion][0]
                downvotes = suggestions_dict[suggestion][1]
                procent = upvotes - downvotes
                pair.append((msg.content.split(' ')[0], procent))
    sorted_suggestions = sorted(pair, key=lambda x: x[1], reverse=True)
    for i, (smsg, sprocent) in enumerate(sorted_suggestions[:10]):
        emb.add_field(name=f"{i+1} место. Разность оценки: {sprocent}", value=smsg, inline=False)
    await slash_inter.edit_original_response(embed=emb)

async def announce(channel_id):
    channel = bot.get_channel(channel_id)
    await channel.send('Теперь вы можете использовать команду >suggest здесь.')
    
########################
@tasks.loop(minutes=10)
async def save():
    exportData(suggestions, service)
    
# {u:{[s:[u,d]]}}
@tasks.loop(seconds=5)
async def check():

    for user in suggestions.keys():
        for user_suggestion in range(len(suggestions[user])):
            suggestions_dict = suggestions[user][user_suggestion]
            for suggestion in suggestions_dict.keys():
                msg = bot.get_message(suggestion)
                for reaction in range(len(msg.reactions)):
                    if(str(msg.reactions[reaction]) == str(service[0])):
                        suggestions_dict[suggestion][0] = msg.reactions[reaction].count
                    if(str(msg.reactions[reaction]) == str(service[1])):
                        suggestions_dict[suggestion][1] = msg.reactions[reaction].count


with open('token.txt', 'r') as file:
    token = file.read()
bot.run(token)