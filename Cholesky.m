% Caricamento della matrice dal file .mat
tmp = load(['Matrix\cfd1.mat']);
A = tmp.Problem.A;

% Creazione del vettore xe
n = size(A, 1);  % Dimensione della matrice
xe = ones(n, 1);

% Calcolo del termine noto b
b = A * xe;

% Decomposizione di Cholesky della matrice A
R = chol(A);

% Risoluzione del sistema Ax = b
% Risolviamo per y nel sistema triangolare inferiore R' * y = b
y = R' \ b;

% Risolviamo per x nel sistema triangolare superiore R * x = y
x = R \ y;

% Visualizziamo la soluzione
disp('Soluzione del sistema Ax = b:');
disp(x);

% Confronto con la soluzione esatta
disp('Soluzione esatta xe:');
disp(xe);

% Verifica dell'errore
errore_relativo = norm(x - xe) / norm(xe);
disp('Errore tra la soluzione calcolata e la soluzione esatta:');
disp(errore);