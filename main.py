import asyncio, discord

client = discord.Client()
user_bot = "BOT" #Put in this variable the bot nickname.
token = "NDQ2ODY5MTI5MDM1NTEzODU2.Dd_ZUA.BTCnz-nVOayq7NJwntornbUz9rA" #Put in this variable the bot token
trust = ["TsunamiRaze㋡#0511", ""] #Put in this variable the users can use restrired commands
trust_roles = ["Owner, Admin, Mod"]
ranks = False

client = discord.Client()
ver = "1.3.0-beta.1"
lang = "en"

print("NextBot " + ver + " " + lang)

@client.event
@asyncio.coroutine
def on_message(message):
    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    user_bot_client = client.user.name
    role_trusted = False
    for role_name in trust_roles:
        if ":" in role_name:
            rank_role = discord.utils.get(message.server.roles, name = ":".join(role_name.split(":")[1:]))
        else:
            rank_role = discord.utils.get(message.server.roles, name = role_name)
        if type(rank_role) is discord.role.Role and rank_role.id in [r.id for r in message.author.roles]:
            role_trusted = True
    trusted = user in trust or role_trusted
    try:
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        pm = False
    except AttributeError:
        server_msg = user
        chan_msg = user
        pm = True
    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""

    print(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep)

    if ranks and not pm:
        open("msgs_user_" + server_msg + ".txt", "a").close()
        msgs = open("msgs_user_" + server_msg + ".txt", "r")
        msgs_r = msgs.read()
        if user not in msgs_r or user != user_bot_client:
            msgs_w = open("msgs_user_" + server_msg + ".txt", "a")
            msgs_w.write(user + ":0\n")
            msgs_w.close()
            msgs.close()
            msgs = open("msgs_user_" + server_msg + ".txt", "r")
            msgs_r = msgs.read()
        msgs_user = msgs_r.split(user + ":")[1]
        msgs.close()
        user_msgs_n = int(msgs_user.split("\n")[0])
        user_msgs_n += 1
        msgs_r = msgs_r.replace(user + ":" + str(user_msgs_n - 1), user + ":" + str(user_msgs_n))
        msgs = open("msgs_user_" + server_msg + ".txt", "w")
        msgs.write(msgs_r)
        msgs.close()

#Beginning of the commands
    if command == "!commandtest": #Copy this code to create a command
        yield from client.send_message(message.channel, "Bot is Online.")

    if command == "!ban" and trusted and not pm: #This command bans an user, "and trusted" means the command is restricted and only trust users can use this command, "and not PM" means this command can't use in PM
        if "<@" in params[1] and ">" in params[1]: #The variable params[1] is the first parameter input by the user. If the first parameter is a mention
            id_user = message.server.get_member(params[1].replace("<@", "").replace(">", "")) #the user ID of the mention is got
        else: #else
            id_user = message.server.get_member_named(params[1]) #the nickname input in the first parameter is got
        try:
            yield from client.ban(id_user, int(params[2])) #this line bans the user with the variable id_user who is the ID user to ban
        except IndexError: #if the number of messages is not put (by typing !ban user), the bot will ban the user but doesn't remove a message
            yield from client.ban(id_user, 0)

    if command == "!ban" and trusted and not pm: 
        id_user = message.server.get_member_named(params[1]) 
        try:
            yield from client.ban(id_user, int(params[2])) #this line bans the user with the variable id_user who is the ID user to ban
        except IndexError: #if the number of messages is not put (by typing !ban user), the bot will ban the user but doesn't remove a message
            yield from client.ban(id_user, 0)

    if command == "!bing": #This command search on Bing
        yield from client.send_message(message.channel, "https://www.bing.com/search?q=" + "+".join(params[1:]))

    if command == "!create_channel" and trusted and not pm: #This command creates a channel on the server, " ".join(params[1:]) is the name of the channel and " ".join() put the words from params[1:] from "params" list which contains all of the words of the message (except the command which is params[0]).
        yield from client.create_channel(message.server, " ".join(params[1:]))

    if command == "!create_channel_voice" and trusted and not pm: #This command creates a vocal channel, see the previous command.
        yield from client.create_channel(message.server, " ".join(params[1:]), type=discord.ChannelType.voice)

    if command == "!google": #See !bing
        yield from client.send_message(message.channel, "https://www.google.com/#q=" + "+".join(params[1:]))

    if command == "!join_channel_voice" and trusted: #This command joins a vocal channel.
        voice_chan = yield from client.join_voice_channel(client.get_channel(params[1]))

    if command == "!quit_channel_voice" and trusted: #This command quits a vocal channel.
        voice_chan.disconnect()

    if command == "!kick" and trusted and not pm: #See !ban
        if "<@" in params[1] and ">" in params[1]:
            id_user = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[1])
        yield from client.kick(id_user)

    if command == "!music" and trusted: #This command reads music, the firsh param is the channel id and the second is the music URL.
        voice_chan = yield from client.join_voice_channel(client.get_channel(params[1])) #This line joins the vocal channel.
        music = yield from voice_chan.create_ytdl_player(" ".join(params[2:])) #This commands gets the music of the URL.
        music.start() #This line diffuses the music.

    if command == "!nick" and trusted and not pm: #Here, there are a command which change the nickname of the bot
        yield from client.change_nickname(client.user, " ".join(params[1:]))

    if (command == "!prune_members" or command == "!purge_members") and trusted and not pm: #This command prunes the inactive members.
        try:
            yield from client.prune_members(message.server, days = int(params[1]))
        except IndexError: #params[1] is the days number of the last connection of members, if the parameter isn't put, the bot prunes members who doesn't connect the 30 last days
            yield from client.prune_members(message.server, days = 30)

    if (command == "!purge" or command == "!clear") and trusted and not pm: #This command clean the messages, by typing !clear 10, the bot will remove the 10 last messages
        yield from client.purge_from(message.channel, limit = int(params[1])) #This line deletes the messages with params[1] which is the first parameter (the messages number), there are int(params[1]) because the parameters must be converted to a number.

    if (command == "!quit" or command == "!exit") and trusted: #This command closes the bot.
        yield from client.close()

    if (command == "!rename_channel" or command == "!nick_channel") and trusted and not pm: #Here, there are a command which change the name of the channel where the message is sent
        yield from client.edit_channel(message.channel, name = " ".join(params[1:]))

    if command == "!role_user_add" and trusted and not pm: #This command gives a role to an user.
        if "<@" in params[1] and ">" in params[1]:
            member = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name = " ".join(params[2:])) #this line get the role, " ".join(params[2:]) is the role name
        yield from client.add_roles(member, role) #this line add the role to the user and member is the ID of the bot

    if command == "!role_user_remove" and trusted and not pm: #This command remove a role from a user.
        if "<@" in params[1] and ">" in params[1]:
            member = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name = " ".join(params[2:]))
        yield from client.remove_roles(member, role)

    if command == "!roles" and trusted and not pm: #This command lists the roles of the server.
        for role in message.server.roles:
            yield from client.send_message(message.channel, role.id + " : " + role.name)

    if command == "!unban" and trusted and not pm: #This command unban an user.
        if "<@" in params[1] and ">" in params[1]:
            id_user = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[1])
        yield from client.unban(message.server, id_user)

    if command == "!say" and trusted:
        yield from client.send_message(client.get_channel(params[1]), " ".join(params[2:]))

    if command == "!say_user" and trusted:
        if params[2].lower() == params[2].upper():
            yield from client.send_message(client.get_server(params[1]).get_member(params[2]), " ".join(params[3:]))
        else:
            yield from client.send_message(client.get_server(params[1]).get_member_named(params[2]), " ".join(params[3:]))

    if command == "!status_game" and trusted: #This command put a game to the client, " ".join(params[1:]) is the game name.
        yield from client.change_presence(game = discord.Game(name = " ".join(params[1:])))

    if (command == "!topic" or command == "!topic_channel") and trusted and not pm: #Here, there are a command which change the nick of the channel
        yield from client.edit_channel(message.channel, topic = " ".join(params[1:]))

    if command == "!ver": #This command send the bot version.
        yield from client.send_message(message.channel, "NextBot " + ver + " " + lang)

    if command == "!viki" or command == "!vikidia": #This command search on Vikidia.
        yield from client.send_message(message.channel, "https://" + params[1] + ".vikidia.org/wiki/" + "_".join(params[2:]))

    if command == "!wp" or command == "!wikipedia": #This command search on Wikipedia.
        yield from client.send_message(message.channel, "https://" + params[1] + ".wikipedia.org/wiki/" + "_".join(params[2:]))

    if "he is cool " + user_bot.lower() in rep.lower(): #Here, the bot can answer to sentences, for example, saying "He is cool NextBot", the bot answer "Thank you, you are also cool !".
        yield from client.send_message(message.channel, "Thank you, you are also cool ! :)")
#End of the commands

client.run(NDQ2ODY5MTI5MDM1NTEzODU2.Dd_ZUA.BTCnz-nVOayq7NJwntornbUz9rA)
