import shutil
import re

from simple_term_menu import TerminalMenu

from abilities import *
from dungeons_and_dragons import *
from cyberpunk_2077 import *
from disco_elysium import *


if __name__ == "__main__":

    menu_width=shutil.get_terminal_size((80,20))[0]

    menu_style={
        "menu_cursor":None,
        "menu_cursor_style":None,  # The style of the shown cursor.
        "menu_highlight_style":(
            "bg_black",
            "bold",
        ),  # The style of the selected menu entry.

        "search_key":None,
        "search_highlight_style":(
            "fg_red",
        ),  # The style of matched search strings.


        "show_shortcut_hints":False,
        "shortcut_key_highlight_style":(
            "fg_cyan",
        ),  # The style of shortcut keys.
        "shortcut_brackets_highlight_style":(
            "fg_gray",
        ),  # The style of parentheses enclosing shortcut keys.

        "cycle_cursor":True,  # A bool value which indicates if the menu cursor cycles when the end of the menu is reached.

        "clear_screen":True,  # A bool value which indicates if the screen will be cleared before the menu is shown.
        "clear_menu_on_exit":True,  # A bool value which indicates if the menu will be cleared after the show method.
    }

    multi={
        "multi_select":True,
        "multi_select_select_on_accept":False,
        "multi_select_cursor":"●",
        "multi_select_cursor_style":None,
        "multi_select_cursor_brackets_style":None,
    }

    game_dict={
        "DungeonsDragons":"Dungeons and Dragons",
        "Cyberpunk2077":"Cyberpunk 2077",
        "DiscoElysium":"Disco Elysium",
    }

    preferred_scores=set()

    game_index=0

    while game_index is not None:
        game_index=TerminalMenu(
            (f"  {value:{menu_width-2}}" for value in game_dict.values()),
            title=f"Choose game:\n",
            cursor_index=game_index,  # The initially selected item index.
        **menu_style).show()

        if game_index is None:
            break

        game=list(game_dict.values())[game_index]

        if game==game_dict["DungeonsDragons"]:
            tier=2

            while tier is not None:
                tier=TerminalMenu(
                    (f"  {value:{menu_width-2}}" for value in DungeonsDragons._names.values()),
                    title=f"{game}: tier\n",
                    cursor_index=tier,  # The initially selected item index.
                **menu_style).show()

                if tier is None:
                    break

                race_index=3

                while race_index is not None:
                    if tier==6:
                        race_index=TerminalMenu(
                            (f"  {'Human':{menu_width-2}}",),
                            title=f"{game}: {DungeonsDragons._names[tier]} race\n",
                            cursor_index=race_index,  # The initially selected item index.
                        **menu_style).show()

                        if race_index is not None:
                            race_index=3

                    else:
                        race_index=TerminalMenu(
                            (f"  {key:{menu_width-2}}" for key in DungeonsDragons._races),
                            title=f"{game}: {DungeonsDragons._names[tier]} race\n",
                            cursor_index=race_index,  # The initially selected item index.
                        **menu_style).show()

                    if race_index is None:
                        break

                    race=list(DungeonsDragons._races)[race_index]

                    subrace_index=0

                    if type(DungeonsDragons._races[race]) is dict:
                        subrace_index=TerminalMenu(
                            (f"  {key:{menu_width-2}}" for key in DungeonsDragons._races[race]),
                            title=f"{game}: {DungeonsDragons._names[tier]} subrace {race}\n",
                            cursor_index=subrace_index,  # The initially selected item index.
                        **menu_style).show()

                        if subrace_index is None:
                            continue

                        subrace=list(DungeonsDragons._races[race])[subrace_index]

                    else:
                        subrace=""

                    extra=0

                    while extra is not None:
                        extra=TerminalMenu(
                            (f"  +{key:<{menu_width-3}}" for key in range(DungeonsDragons._max_extra+1)),
                            title=f"{game}: {DungeonsDragons._names[tier]} {subrace} {race} extra\n",
                            cursor_index=extra,  # The initially selected item index.
                        **menu_style).show()

                        if extra is None:
                            break

                        scores_list=[
                            f" {key:<{menu_width-1}}" for key in str(DungeonsDragons(tier,race,subrace,extra)).split("\n")
                        ]
                        scores_index=0

                        while scores_index is not None:
                            scores_index=TerminalMenu(
                                scores_list,
                                title=f"{game}: {DungeonsDragons._names[tier]} {subrace} {race} +{extra} ({len(scores_list)})\n",
                                cursor_index=scores_index,  # The initially selected item index.
                            **menu_style).show()

                            if scores_index is None:
                                break

                            scores_list[scores_index]=re.sub("^ ","●",scores_list[scores_index])
                            preferred_scores.add(scores_list[scores_index])

        if game==game_dict["Cyberpunk2077"]:
            level=0

            while level is not None:
                level=TerminalMenu(
                    (f"  {f'{key+1:02}':<{menu_width-2}}" for key in range(Cyberpunk2077._max_level)),
                    title=f"{game}: level\n",
                    cursor_index=level,  # The initially selected item index.
                **menu_style).show()

                if level is None:
                    break

                scores_list=[
                    f" {key:<{menu_width-1}}" for key in str(Cyberpunk2077(level+1)).split("\n")
                ]
                scores_index=0

                while scores_index is not None:
                    scores_index=TerminalMenu(
                        scores_list,
                        title=f"{game}: Level {level+1} ({len(scores_list)})\n",
                        cursor_index=scores_index,  # The initially selected item index.
                    **menu_style).show()

                    if scores_index is None:
                        break

                    scores_list[scores_index]=re.sub("^ ","●",scores_list[scores_index])
                    preferred_scores.add(scores_list[scores_index])

        if game==game_dict["DiscoElysium"]:
            scores_list=[
                f" {key:<{menu_width-1}}" for key in str(DiscoElysium()).split("\n")
            ]
            scores_index=0

            while scores_index is not None:
                scores_index=TerminalMenu(
                    scores_list,
                    title=f"{game}: ({len(scores_list)})\n",
                    cursor_index=scores_index,  # The initially selected item index.
                **menu_style).show()

                if scores_index is None:
                    break

                scores_list[scores_index]=re.sub("^ ","●",scores_list[scores_index])
                preferred_scores.add(scores_list[scores_index])

    for scores in sorted(preferred_scores):
        print(scores)
