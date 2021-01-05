from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import cfscrape
import requests
import asyncio

# Your mod page URL
URL = 'https://www.planetminecraft.com/mod/minecraft-earth-mod/'
# https://www.curseforge.com/minecraft/mc-mods/minecraft-earth-mod
# The URL above is my mod URL

target_url = "https://www.planetminecraft.com/mod/minecraft-earth-mod/"   # replace url with anti-bot protected website
scraper = cfscrape.create_scraper(delay=10)
html_text = scraper.get(target_url).text
actualpage = BeautifulSoup(html_text, 'html.parser')
# print(actualpage.prettify())
# print(actualpage.a)
print("Currently Accessing: " + actualpage.title.string)
# print(actualpage.find(id='widget-submissions'))
#for x in actualpage.find_all(id='widget-submissions'):
#	print(x.get('href'))

latestcomment = actualpage.find(class_="forum_reply")
latestcommenttext = latestcomment.find(class_="contents pmc_readmore").get_text()
emeraldscore = latestcomment.find(class_="score").get_text()
timepublished = "Published On: " + latestcomment.find(class_="time_box").findChild().text
PMCuserlevel = latestcomment.find(class_="rank_box").findChild(class_="member_level").text
usericon = latestcomment.findAll('img')
PMCuserName = latestcomment.findAll('a')
for image in usericon:
    usericon = image['data-src']
    break
for username in PMCuserName:
	PMCuserName = username['href'][8:-1]
	break
print(latestcommenttext)
print(PMCuserlevel)
print(emeraldscore)
print(usericon)
print(PMCuserName)
print(timepublished)

channel = '1'

client = commands.Bot(command_prefix="p!")

# Something that just opens a token file I used for privacy, you do not have to use this line
with open('token.txt') as token:
    tk436 = token.readline()

@client.event
async def on_ready(): 
    print('Bot Connected!')

@client.event
async def on_disconnect():
	print('Disconnected!')

@client.command()
async def latestcomment(ctx):
	embed = commentbuilder()
	print('sent!')
	await ctx.send(embed=embed)

@client.command()
async def hi(ctx):
	await ctx.send("hi")

@client.command()
async def setchannel(ctx):
	with open("channel.txt", 'w') as x:
		x.write(str(channel))

async def updatecomment():
	while True:
		tempcomment = actualpage.find(class_="forum_reply")
		global latestcomment
		# print("test")
		if (tempcomment!=latestcomment):
			print("New Comment Detected!")
			latestcomment = tempcomment
			latestcommenttext = latestcomment.find(class_="contents pmc_readmore").get_text()
			emeraldscore = latestcomment.find(class_="score").get_text()
			timepublished = "Published On: " + latestcomment.find(class_="time_box").findChild().text
			PMCuserlevel = latestcomment.find(class_="rank_box").findChild(class_="member_level").text
			usericon = latestcomment.findAll('img')
			PMCuserName = latestcomment.findAll('a')
			for image in usericon:
			    usericon = image['data-src']
			    break
			for username in PMCuserName:
				PMCuserName = username['href'][8:-1]
				break
		await asyncio.sleep(10)

def commentbuilder():
	embed=discord.Embed(title="Latest Comment", url="https://www.planetminecraft.com/mod/minecraft-earth-mod/", color=0xff7b00)
	embed.set_thumbnail(url=usericon)
	embed.add_field(name="User " + PMCuserName + " says...", value=latestcommenttext, inline=False)
	embed.add_field(name="User Level", value=PMCuserlevel)
	embed.add_field(name="Emeralds on Comment", value=emeraldscore)
	embed.set_footer(text = timepublished)
	return embed

client.loop.create_task(updatecomment())

# Replace the "tk436" with your own bot token     
client.run(tk436)
