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
        ""
        ]
"""
Stages:
    0: Overall cost
    1: Pals excluded
    2: For each pal, how much are they excluded from the total cost

"""
stages = 3 # No. of stages + 1

# Initialize a dictionary to store user answers
answers = {}
excludeds = {}

@bot.command()
@commands.guild_only()
async def dinner(ctx):
    global answers
    global excludeds
    answers = {}
    excludeds = {}


    await ctx.author.send("Process started, send '/q' to stop at any time.")
    # Iterate over each question
    # for question in questions:
    for stage in range(stages):
        stageContinue = False
        notStop = True
        while (not stageContinue) and notStop:
            match stage:
                case 0:
                    # How much did you spend?
                    await ctx.author.send(questions[0])
                case 1:
                    # Is anyone excluded, out of:
                    tmp = questions[1]
                    for field in data_json.keys():
                        tmp += field + ", "
                    tmp += "\n For example: `bob, jerry, nick`"
                    tmp += "\n If none, type 'none'"
                    await ctx.author.send(tmp)
                case 2:
                    # For each person excluded, how much are they excluded from the total cost?
                    # Then perform last check
                    print(len(excludeds))
                    await getExclusions(ctx)


                    tmp = "Ok, so just to check: You spent " + str(answers[0]) + ", "
                    if answers[1] == "none":
                        tmp += "everyone is included"
                    else:
                        if (len(excludeds) == 1):
                            for name in excludeds:
                                tmp += str(name) + " was not included with $" + str(excludeds[name])
                        else:
                            for name in excludeds:
                                tmp += str(name) + ", "
                                tmp += " was excluded with $" + str(excludeds[name]) + ", "
                    tmp += "\n If the above is correct, type `yay`, otherwise `nay`"
                    await ctx.author.send(tmp)
                    pass

            # Store the user's answer, stop on /stop
            def check(m):
                return m.author == ctx.author #and m.channel == ctx.channel
            response = await bot.wait_for('message', check=check, timeout=60)

            match await getResponse(stage, check, response):
                case 0:
                    # Continue
                    stageContinue = True
                case 1:
                    # /stop command called
                    notStop = False
                case 2:
                    # invalid response
                    stageContinue = False
                    await ctx.author.send("Whoops, that doesn't sound right")
                    


    # Display the collected answers
    await ctx.author.send("All done, and all recorded! You can check your account with these commands which are yet to be implemented.")

async def getResponse(stage, check, response):
    global excludeds
    if response.content.lower() == '/stop':
        return 1
    else:
        match stage:
            case 0:
                # How much total
                if not response.content.replace("$", "").isdigit():
                    # Non-numeric answer
                    return 2
            case 1:
                # Excluded people
                if response.content.lower() != "none":
                    tmp = response.content.lower().split(",")
                    tmp = [s.strip() for s in tmp]
                    if (all(name in list(data_json.keys()) for name in tmp)):
                        excludeds = {key: 0 for key in tmp}
                    else:
                        return 2
            case 2:
                # For each person in excludeds, how much are they excluded by
                pass


        answers[stage] = response.content
        return 0

async def getExclusions(ctx):
    for person in excludeds:
        stageContinue = False
        while not stageContinue:
            tmp = "For " + person + ", how much are they excluded from the total $" + str(answers[0]) + "?"
            await ctx.author.send(tmp)
            def check(m):
                return m.author == ctx.author #and m.channel == ctx.channel
            response = await bot.wait_for('message', check=check, timeout=60)

            if response.content.isdigit():
                excludeds[person] = response.content
                stageContinue = True
            else:
                stageContinue = False
                await ctx.author.send("Whoops, that doesn't sound right")


# Run the bot
bot.run(str(TOKEN))
