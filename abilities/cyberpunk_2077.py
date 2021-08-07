from abilities import *


class Cyberpunk2077(Abilities):

    """ Specialized Abilities class for Dungeons and Dragons.

    Not only it includes the special D&D score schemas,
    but implements augmenting printed scores with chosen race specific modifiers.

    Static Attrtibutes:
        _names: names for D&D score schemas
        _schemas: the D&D score schemas (see Abilities class)
        _races: the augmenting patterns for each race and subrace in D&D
        _level: the augmenting patterns for leveling up characters (at attribute-iincreasing milestones)
    """


    _definition=[3,6]
    _extent=5

    _min_level=1
    _max_level=50


    def __init__(self,level:int=1):

        """ Generate a new Cyberpunk 2077 attribute score system.

        Arguments:
            level: additional ability points
                default: 0
        """


        super().__init__(Schema(definition=Cyberpunk2077._definition),Cyberpunk2077._extent)

        if level-1:
            level=min(max(level,Cyberpunk2077._min_level),Cyberpunk2077._max_level)

            _levels=Abilities(Schema([0,level-1]),Cyberpunk2077._extent,cutoff=level-1)
            _augmentations=set()

            for augmentation in _levels:
                _augmentations.update(itertools.permutations(augmentation,Cyberpunk2077._extent))

            super().augment(_augmentations)


    def __str__(self)->str:

        """ Wrapper for Abilities print with mod 3 for skill unlocking checkpoints.
        """


        return super().__str__(spectrum=set(range(1,21)),mod=2)
