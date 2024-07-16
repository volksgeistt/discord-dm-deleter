import discord
from discord.ext import commands
import asyncio
import colorama
from colorama import Fore

client = commands.Bot(command_prefix="!", self_bot=True, help_command=None)

async def msgDeleteWorker(userID):
    try:
        user = await client.fetch_user(userID)
        dm = await user.create_dm()
        taskToDelete = 0
        while True:
            messages = await dm.history(limit=100).flatten()
            if not messages:
                break
            task = [ asyncio.create_task(message.delete()) for message in messages if message.author == client.user ]
            if task:
                await asyncio.gather(*task)
                taskToDelete += len(task)
                print(f"{Fore.GREEN} [ LOG ] : DELETED {len(task)} DM MESSAGES..! Total: {taskToDelete} {Fore.RESET}")
            await asyncio.sleep(0.1)
        print(f"{Fore.GREEN} [ LOG ] : Finished DELETING MESSAGES..! Deleted Total: {taskToDelete} {Fore.RESET}")
    except discord.errors.Forbidden:
        print(f"{Fore.RED} [ LOG ] : Can't DELETE MESSAGES In User DMs With ID {userID}. {Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED} [ LOG ] : ERROR OCCURED -> {e} {Fore.RESET}")

@client.event
async def on_ready():
    print(f'\n{Fore.YELLOW} [ LOG ] : LOGGED IN AS {client.user} {Fore.RESET}')
    print('------')
    userID = int(input(f"\t{Fore.MAGENTA} [ LOG ] : Enter USER ID To Delete DMs With ->  {Fore.RESET}"))
    await msgDeleteWorker(userID)

@client.command()
async def ping(ctx):
    await ctx.send(f"{int(client.latency*1000)} ms")

if __name__ == "__main__":
    token = input(f"{Fore.MAGENTA} [ LOG ] : Enter Your ACCOUNT TOKEN ->  {Fore.RESET}")
    client.run(token, bot=False)
