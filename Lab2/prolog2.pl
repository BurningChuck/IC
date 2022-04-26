%Facts
man('Ivan').
man('Sanya').
man('Petro').
man('Sam').
man('Sem').
man('Tadei').
man('Taras').
man('Tom').
woman('Ann').
woman('Oksana').
woman('Kate').
woman('Ira').
woman('Inna').
woman('Dasha').
woman('Angelina').
parent('Ann','Ivan').
parent('Ann','Sanya').
parent('Petro','Ivan').
parent('Petro','Sanya').
parent('Ivan', 'Kate').
parent('Oksana', 'Kate').
parent('Inna','Oksana').
parent('Inna','Ira').
parent('Ira','Tadei').
parent('Sem','Oksana').
parent('Sem','Ira').
parent('Ivan','Sam').
parent('Oksana','Sam').
parent('Sem','Oksana').
parent('Tom','Dasha').
parent('Dasha','Angelina').
parent('Tadei','Angelina').
parent('Taras','Tadei').
marriage('Oksana','Ivan').
marriage('Ann','Petro').
marriage('Inna','Sem').
marriage('Dasha','Tadei').
marriage('Ira','Taras').

%Rules
father(X,Y):-man(X), parent(X,Y).
mother(X,Y):-woman(X),parent(X,Y).
husband_mother(X,Y):-mother(X,Z),marriage(Y,Z),woman(Y).
wife_mother(X,Y):-mother(X,Z),marriage(Y,Z),man(Y).
brother(X,Y):-man(X),parent(Z,X),parent(Z,Y),not(X=Y).
sister(X,Y):-woman(X),parent(Z,X),parent(Z,Y),not(X=Y).
uncle(X,Y):-man(X),brother(X,Z),parent(Z,Y).
aunt(X,Y):-woman(X),brother(X,Z),parent(Z,Y).
grandpa(X,Y):-man(X),parent(X,Z),parent(Z,Y). 
grandma(X,Y):-woman(X),parent(X,Z),parent(Z,Y).
bro_or_sis(X,Y):-parent(Z,X),parent(Z,Y),not(X=Y).
cousin(X,Y):-parent(Z,X),parent(A,Y),bro_or_sis(Z,A).