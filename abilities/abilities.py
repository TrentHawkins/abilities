from __future__ import annotations

import itertools
import math

from collections import Counter

from typing import Iterable
from typing import Optional
from typing import Union


def int_str(entry:Union[int,tuple[int]],referrence:Optional[int]=None):

    """ Return whitespace-separated values of input container.

    Arguments:
        input: item to print in one line usually a list

    Returns:
        formatted string with adaptive integer width
    """


    if type(entry) is int:
        entry=(entry,)

    if referrence: width=int(math.log10(referrence))+1 if referrence else 1
    else:          width=int(math.log10(sum(entry)))+1 if sum(entry) else 1

    return " ".join((f"{item if item else '':{width}}" for item in entry))


class Schema(dict[int:int]):

    """ A Counter dictionary connecting a score to its cost.

    Counter is used to facilitate the merging of two schemas.

    Example:
        The Dungeons and Dragons standard dict definition={
             8:0,  # ground score containing the extent instead of cost (trivially cost 0)
            13:1,  # score where cost 1 ends
            15:2,  # score where cost 2 ends
        } says that starting from ground score 8,the first 5 increments cost 1 point and the next 2 cost 2.
        You can skip a particular cost by repeating the previous score.
        The class then translates it into a dictionary point cost schema={
             8:0,  # ground score with cost 0
             9:1,
            10:2,
            11:3,
            12:4,
            13:5,  # score where cost 1 ends
            14:7,
            15:9,  # score where cost 2 ends
        } that we know from the Player's Handbook,which is then used to produce all possible combinations,
        given a cost cutoff. A default cost cutoff is evaluated as half the cost volume defined in the original schema,
        as evaluated by the input list schema.

    Operators:
        __add__: add two schemas by not only uniting their keys but adding all combinations of sums between them
        __mul__: effectively repeat __add__ on one schema as many times as specified
    """


    def __init__(self,definition:Optional[Union[dict[int:int],list[int]]]=None):

        """ Generate a set of scores out of schema out of a definition.

        The definition should be a list with positive integers indicating the gradually increasing costs.

        The value at 0 should indicate the ground ability score in the schema
        that the increments represented by the other values build on.

        Arguments:
            definition: list of cost progression check points or the dictionary itself
                default: empty schema that can be filled as a dictionary
        """


        if not definition:
            super().__init__()

        elif isinstance(definition,dict):
            super().__init__(definition)

        elif isinstance(definition,list):
            definition.sort()
            cost=0

            super().__init__({definition[0]:cost})

            for base_checkpoint,next_checkpoint in zip(definition[:-1],definition[1:]):
                cost+=1

                for score in range(base_checkpoint,next_checkpoint):
                    self[score+1]=self[score]+cost


    def __add__(self,other:Schema)->Schema:

        """ Add two schemas by adding all combination of keys of sums between them.

        Arguments:
            other: another Schema

        Returns:
            sum of the two schemas
        """


        _add=Schema()

        for self_score,other_score in itertools.product(self,other):
            _score=self_score+other_score
            _add[_score]=max(_add.get(_score,0),self[self_score]+other[other_score])

        return _add


    def __mul__(self,times:int)->Schema:

        """ Add a schema many times.

        Arguments:
            times: how many times to add schema

        Returns:
            the same schema added several times
        """


        _mul=Schema()

        for time in range(times):
            _mul+=self

        return _mul


    def __str__(self)->str:

        """ Print schema.

        Returns:
            Fully expanded schema with costs and cost-increments too.
        """

        _str="\n"

        for score in self:
            _str+=(
                f" score {int_str(     score ,referrence=max(self.keys(  )))}"
                f" cost { int_str(self[score],referrence=max(self.values()))}"
                f" step +{int_str(self[score]-self.get(score-1,0))}\n"
            )

        return _str


class Scores(tuple[int]):

    """ Scores are lists of integers. They are augmented with the following common operations on score palettes (lists).

    Operators:
        __add__: add two score palettes element-wise
        __mul__: multiply a score palette many times
        __mod__: count how many scores are divisible by argument

    Methods:
        distribution: the distribution of given scores across the spectrum
        pattern: counting of the distribution values
    """


    def __add__(self,other:Scores)->Scores:

        """ Add two score palettes element-wise.

        Arguments:
            other: another score palette

        Returns:
            the sum of two score palettes along with their schemas
        """


        return Scores(sorted(self_score+other_score for self_score,other_score in zip(self,other)))


    def __mul__(self,times:int)->Scores:

        """ Multiply a score palette times an integer (in consistency with __add__).

        Arguments:
            times: how many times to add score palette

        Returns:
            the same score palette added several times
        """


        return Scores(score*times for score in self)


    def __mod__(self,times:int)->int:

        """ Count how many scores are divisible by times.

        Arguments:
            times: base of multiples scores are checked against

        Returns:
            count of scores with zero residual on times
        """


        return sum(1 for score in self if score%times==0)


    def distribution(self,spectrum:set[int])->list[int]:

        """ Get the distribution of given scores across the spectrum given.

        Arguments:
            spectrum: a set of possible scores for the distribution

        Returns:
            a list of counts in score palette for each score in schema
        """


        return list(Counter(self)[score] for score in spectrum)


    def pattern(self,distribution:list[int])->list[int]:

        """ Get the distribution of given counts across the score distribution given.

        Arguments:
            distribution: a list of counts of scores

        Returns:
            a list of counts in score palette for each score in schema
        """


        return list(Counter(distribution)[count+1] for count in range(len(self)))


    def __str__(self,spectrum:set[int]=set(),mod:int=1)->str:

        """ Print one line with scores and optionally statistics for the scores if internally used.

        Arguments:
            spectrum: a set of possible scores for teh distribution
            mod: base of multiples scores are checked against

        Returns:
            scores with their sum plus statistics if called internally
        """


        return (
            f" scores {      int_str(                 self                         )}"
            f" sum {         int_str(sum(             self                        ))}"
            f" mod {         int_str(                 self%mod                     )}"
            f" type {        int_str(sum(self.pattern(self.distribution(spectrum))))}"
            f" pattern {     int_str(    self.pattern(self.distribution(spectrum)) )}"
            f" distribution {int_str(                 self.distribution(spectrum)  )}"
        )


class Abilities(set):

    """ Expands an attribute score schema to all possible attribute score palettes.

    Attributes:
        _fitted: weather default palettes have been evaluated
        _schema: dict with costs of scores
        _extent: number of attributes in ability score system
        _cutoff: a custom cutoff for the cost of viable score palettes

    Methods:
        fit: evaluate the scores in an attributes system

    Operators:
        __str__: print all available score palettes given cutoff
    """


    def __init__(self,schema:Schema,extent:int,cutoff:Optional[int]=None):

        """ Abilities constructor.

        Arguments:
            schema: a dictionary with costs on scores
                default: create an empty score system
            extent: number of attributes in ability score system
                default: create an empty score system
            cutoff: a custom cutoff for the cost of viable score palettes
                default: half the maximum cost defined by the schema
        """


        self._schema=schema
        self._extent=extent

        if cutoff:
            self._cutoff=cutoff

        else:
            self._cutoff=(self._extent*max(self._schema.values()))//2  # default cost cutoff for determining viable score palettes

        super().__init__()

        for scores in itertools.combinations_with_replacement(self._schema,self._extent):
            if sum(self._schema[score] for score in scores)==self._cutoff:  # NOTE:check case with residual cost
                self.add(Scores(scores))


    def augment(self,augmentations:set[int]):

        """ Evaluate the scores in an attributes system with an optional augmentation score palette.

        Example:
            When selecting a race and subrace in D&D one gets usually a +2 and a +1 anywhere in their score palette.

        Arguments:
            augmentations: a score palette containing the ne augmentation to mixin (see example)

        Returns:
            a set of all viable (augmented or not) scores
        """


        _augmented=set()

        while self:
            scores=self.pop()
            _augmented.update(scores+augmentation for augmentation in augmentations)

        self.update(_augmented)


    def __str__(self,spectrum:Optional[set[int]]=None,mod:int=1)->str:

        """ Print a score palette along with its various statistics.

        Statistics:
            distribution: the distribution of given scores across the spectrum
            pattern: counting of the distribution values
            type: counting of the pattern values showing how many distinct values are in score palette
        """


        if not spectrum:
            spectrum=self._schema

#       _str=f"\n extent {self._extent}\n cutoff {self._cutoff}\n {self._schema}\n"
#       _str=""

#       for scores in sorted(self):
#           if max(scores) in spectrum:
#               _str+="\n"+scores.__str__(spectrum,mod)

        return "\n".join(scores.__str__(spectrum,mod) for scores in sorted(self) if max(scores) in spectrum)
