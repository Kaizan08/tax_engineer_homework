1st commit: Made tests for the logic portion of the application and made sure they run.
2nd commit: Large refactor to simplify using a Player model that decouples some of the logic and makes it easier to read.
3rd commit: Fixed and added tests and fixed bug


Additional things I would like to add, some of the refactor with the new code for House Rule 2 needs
to be refactored again to pull out some of the specific game types into own comparison function to streamline code
I duplicated some code in order to work on the House Rules 2

Unclear if in House Rule 2 the directions say
King and Queen are played at the same time(which I am taking to mean P1 has a King and P2 has a Queen)
Then do the rules. 

It could be inferred that P1 and P2 are just named King and Queen(which would be odd) and then follow the rules.
Changing this up as now that I'm thinking of it, that would rarely be the case.

Got partially through the second challenge messily, it's not fully functional, and a few things I would typically update, but I'm close to time.
To run tests:

- python3 -m unittest