import discord, json, os
from dotenv import load_dotenv
from discord.ext import commands


#------------------------------------------------------------------------------------
# Load Discord bot API token via dotenv (via .env)
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

#------------------------------------------------------------------------------------
# Load names.list and generate a `data.json` file with those names
if not os.path.exists("./data.json"):
    with open('names.list', 'r') as fs:
        content = fs.readlines()[1].rstrip();
        names = content.split(", ")

        data_json = {}
        for i, obj in enumerate(names):
            gen_pay_list = {}
            for j, sub_obj in enumerate(names):
                if sub_obj != obj:
                    # Set default pay value to 0, obviously ;)
                    gen_pay_list[sub_obj] = 0
            gen_pay_list['earned'] = 0
            data_json[obj] = gen_pay_list

        # Write to data.json
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps(data_json, indent=4))
            print("Debt data file created!")

#------------------------------------------------------------------------------------
# TODO:
# Setup function: call /setup to set up friends list



#------------------------------------------------------------------------------------
# Load data.json names
with open('data.json', 'r') as fs:
    data_json = json.load(fs)

#------------------------------------------------------------------------------------


# Initialize the bot
# Need to choose specific intents

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Define questions
questions = [
        "How much did you spend?",
        "Is anyone excluded, out of ",
        "For x, how much is excluded?"
        ]
"""
Stages:
    0: Overall cost
    1: Pals excluded
    2: For each pal, how much are they excluded from the total cost

"""
stages = 0

# Initialize a dictionary to store user answers
answers = {}

@bot.command()
@commands.guild_only()
async def start_questions(ctx):
    await ctx.send("Process started, send '/q' to stop at any time.")
    # Iterate over each question
    # for question in questions:
    for stage in range(stages):
        match stage:
            case 0:
                # How much did you spend?
                await ctx.send(questions[0])
            case 1:
                # Is anyone excluded, out of:
                tmp = questions[1]
                for field in data_json.keys():
                    tmp += field + ", "
                tmp += " for example: bob, jerry, nick"
                await ctx.send(tmp)
            case 2:
                # For each person excluded, how much are they excluded from the total cost?
                tmp = questions[2] + "(" + str(answers[0]) + ")?"
                await ctx.send(tmp)
                pass

                # Wait for the user's response
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Store the user's answer, stop on /stop
        response = await bot.wait_for('message', check=check, timeout=60)
        if response.content.lower() == '/stop':
            break;
        else:
            answers[stage] = response.content

    # Display the collected answers
    await ctx.send("Thank you for answering the questions! Here are your answers:")
    for question, answer in answers.items():
        await ctx.send(f"{question}: {answer}")

# Run the bot
bot.run(str(TOKEN))
