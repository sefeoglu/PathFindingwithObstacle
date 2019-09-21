#include <incmode>.
%% Generate
#program base.
direction (X,Y) :- X = -1..1 , Y = -1..1 , |X + Y|=1.
at(X,Y,0) :- robot(X,Y).
robot_path(X,Y,0) :- robot(X,Y).
#program step(s).
{robot_path(X2,Y2,s)} :- robot_path(X1,Y1,s-1), field(X1,Y1),field(X2,Y2),direction(X2-X1,Y2-Y1),not obstacle(X2,Y2).
%%Test
#program check(s).
:- query(s), goal(X,Y), not robot_path(X,Y,s).
%% Display
#show robot_path/3.
