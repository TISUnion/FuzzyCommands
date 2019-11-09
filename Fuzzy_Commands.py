# -*- coding: utf-8 -*-
import json
from difflib import SequenceMatcher


PluginName = 'fuzzy_command_args'
ConfigFileFolder = 'config/'
ConfigFilePath = ConfigFileFolder + PluginName + '.json'
command_args = []


def simple_string_matching(a, b):
    return SequenceMatcher(None, a, b)


def onServerInfo(server, info):
    if not info.isPlayer:
        return
    if not info.content.startswith('!!'):
        return
    load_command_args()
    arg = info.content.lstrip('!')
    i = arg.find(' ')
    if i == 0:
        return
    elif i == -1:
        base_arg = arg
        sub_arg = ''
    else:
        base_arg = arg[0:i - 1]
        sub_arg = arg[i:]
    if command_args.count(base_arg) > 0:
        return

    ranked_args = []
    matching_rate = {}
    calc_arg_matching_rate(base_arg, ranked_args, matching_rate)
    if len(ranked_args) == 0:
        return
    first_matching = ranked_args[0]

    fuzzized_args = []
    r0 = 0.5                                                                # r0为宽容限度
    for x in ranked_args:
        if r0 < matching_rate[x]:
            fuzzized_args.append(x)
        else:
            break

    tell_list = []
    for x in fuzzized_args:
        s = '!!' + x + sub_arg + "  --@matching rate " + str(int(100 * first_matching[x])) + "%"
        s = get_text_say(s, '!!' + x + sub_arg)
        tell_list.append(s)
    finalize(server, tell_list, info.content, info.player)


def load_command_args():
    global command_args
    with open(ConfigFilePath, 'r') as f:
        js = json.load(f)
        command_args = js["serverList"]
    return


def calc_arg_matching_rate(arg, rank_list, matching_rate):
    for x in command_args:
        r = simple_string_matching(arg, x)
        matching_rate.update[x] = r
    rank_list = sorted(matching_rate, key=matching_rate.__getitem__)


def get_text_say(text, message):
    return '{"text":"       ","extra":[' + '{"text":"[' + text + ']",\
        "clickEvent":{"action":"suggest_command",\
        "value":"' + message + '"}}]'


def finalize(server, tell_list, init_arg, player_name):
    server.execute('/tellraw ' + player_name + 'Wrong arguments for \"' + init_arg + '\"')
    server.execute('/tellraw ' + player_name + 'You might want to send:')
    for x in tell_list:
        server.execute('/tellraw ' + player_name + x)
    return
