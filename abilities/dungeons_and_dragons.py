from abilities import *


class DungeonsDragons(Abilities):

    """ Specialized Abilities class for Dungeons and Dragons.

    Not only it includes the special D&D score schemas,
    but implements augmenting printed scores with chosen race specific modifiers.

    Static Attrtibutes:
        _names: names for D&D score schemas
        _schemas: the D&D score schemas (see Abilities class)
        _races: the augmenting patterns for each race and subrace in D&D
        _level: the augmenting patterns for leveling up characters (at attribute-iincreasing milestones)
    """


    _names={
        0:"minimal",
        1:"decreased",
        2:"standard",
        3:"increased",
        4:"maximal",
        5:"overkill",
        6:"human-only",
    }
    _definitions={
        0:[12,13   ],
        1:[10,13,14],
        2:[ 8,13,15],
        3:[ 6,13,16],
        4:[ 4,13,17],
        5:[ 2,13,18],
        6:[ 0,13,19],
    }
    _extent=6

    _min_extra=0
    _max_extra=14

#       races                                        S D C I W C
#           subraces                                 T E O N I H
#                        modifiers                   R X N T S A
    _races={
#       "-"             :set(itertools.permutations((0,0,0,0,0,0),6)),
        "Dwarf"     :{
            "Hill"      :set(itertools.permutations((0,0,2,0,1,0),6)),
            "Mountain"  :set(itertools.permutations((2,0,2,0,0,0),6)),
        },
        "Elf"       :{
            "High"      :set(itertools.permutations((0,2,0,1,0,0),6)),
            "Wood"      :set(itertools.permutations((0,2,0,0,1,0),6)),
            "Dark"      :set(itertools.permutations((0,2,0,0,0,1),6)),
        },
        "Halfling"  :{
            "Lightfoot" :set(itertools.permutations((0,2,0,0,0,1),6)),
            "Stout"     :set(itertools.permutations((0,2,1,0,0,0),6)),
        },
        "Human"         :set(itertools.permutations((1,1,1,1,1,1),6)),
        "Dragonborn"    :set(itertools.permutations((2,0,0,0,0,1),6)),
        "Gnome"     :{
            "Forest"    :set(itertools.permutations((0,1,0,2,0,0),6)),
            "Rock"      :set(itertools.permutations((0,0,1,2,0,0),6)),
        },
        "Halfelf"       :set(itertools.permutations((1,0,1,0,0,2),6)),
        "Halforc"       :set(itertools.permutations((2,0,1,0,0,0),6)),
        "Tiefling"      :set(itertools.permutations((0,0,0,1,0,2),6)),
    }


    def __init__(self,tier:int=2,race:Optional[str]=None,subrace:Optional[str]=None,extra:int=0):

        """ Generate a new D&D attribute score system.

        Arguments:
            tier: level of D&D point-by expanse with 0 containing the trivial median (12,12,12,13,13,13) only
                default: Dungeons and Dragons standard
            race: modifiy score palettes with possibilities infered from chosen race
                default: vanilla score palettes
            subrace: refine the race modifier with subrace specifics when applicable
                default: no subrace modifications apply
            class: define maximum allowable levelling-up attribute points
                The actual chosen number can vary, according to user levellin-up choices
            extra: additional ability points
                default: 0
        """


        super().__init__(Schema(definition=DungeonsDragons._definitions[tier]),DungeonsDragons._extent)

        if race:
            if subrace:
                super().augment(DungeonsDragons._races[race][subrace])

            else:
                super().augment(DungeonsDragons._races[race])

        if extra:
            extra=min(max(extra,DungeonsDragons._min_extra),DungeonsDragons._max_extra)

            _extras=Abilities(Schema([0,extra]),DungeonsDragons._extent,cutoff=extra)
            _augmentations=set()

            for augmentation in _extras:
                _augmentations.update(itertools.permutations(augmentation,DungeonsDragons._extent))

            super().augment(_augmentations)


    def __str__(self)->str:

        """ Wrapper for Abilities print with mod 2 for even scores.
        """


        return super().__str__(spectrum=set(range(1,21)),mod=2)
