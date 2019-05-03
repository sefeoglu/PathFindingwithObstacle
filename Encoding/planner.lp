#include <incmode>.
%% Generate
#program base.
direction (X ,Y ) :- X = -1..1 , Y = -1..1 , |X+ Y |=1.
at(X,Y,0) :- robot(X,Y).
robot_path(robot(X,Y),0) :- robot(X,Y).
#program step(s).
{robot_path(robot(X2,Y2),s)} :- robot_path(robot(X1,Y1),s-1), field(X1,Y1),field(X2,Y2),direction(X2-X1,Y2-Y1),not obstacle(X2,Y2).
at(X,Y,s) :- robot_path(robot(X,Y),s).
%%Test
#program check(s).
:- query(s), goal(X,Y), not at(X,Y,s).
#minimize{0,s:at(X,Y,s)}.
%% Display
#show at/3.
