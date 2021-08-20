from abilities import *


class Cyberpunk2077(Abilities):

    """ Specialized Abilities class for Cyberpunk.
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

        """ Wrapper for Abilities print with mod 2 for skill unlocking checkpoints.
        """


        return super().__str__(spectrum=set(range(1,21)),mod=2)
