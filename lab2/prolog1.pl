male(Jake).
male(Terry).
male(Raymond).
male(Charles).
male(Hithckock).
male(Scully).
male(Jakes_Dad).
male(Kevin).
male(Cheddar).



female(Amy).
female(Rosa).
female(Gina).
female(Kelly).
female(megan).
female(savanna).
female(aila).

parent(Jakes_Dad, Jake).
parent(Raymond, Cheddar).
parent(Kevin, Cheddar).
parent(Savanna, Scully).
parent(Megan, Hithckock).
parent(Kelly, Scully).

mother(X, Y) :- parent(X, Y), female(X).
father(X, Y) :- parent(X, Y), male(X).
son(X, Y) :- parent(Y, X), male(X).
daughter(X, Y) :- parent(Y, X), female(X).

descendant(X, Y) :- parent(Y, X); parent(Z, X), descendant(Z, Y).
