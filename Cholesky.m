% Caricamento della matrice dal file .mat
tmp = load(['Matrix\cfd2.mat']);
start_memory = memory;
A = tmp.Problem.A;

% Creazione del vettore xe
n = size(A, 1);  % Dimensione della matrice
xe = ones(n, 1);

tic;

% Calcolo del termine noto b
b = A * xe;

% Decomposizione di Cholesky della matrice A
R = chol(A);

% Risoluzione del sistema Ax = b
% Risolviamo per y nel sistema triangolare inferiore R' * y = b
y = R' \ b;

% Risolviamo per x nel sistema triangolare superiore R * x = y
x = R \ y;

time = toc;
final_memory = memory;

% Visualizziamo la soluzione
disp('Soluzione del sistema Ax = b:');
disp(x);

% Confronto con la soluzione esatta
%disp('Soluzione esatta xe:');
%disp(xe);

% Verifica dell'errore
errore_relativo = norm(x - xe, 2) / norm(xe, 2);
disp('Errore tra la soluzione calcolata e la soluzione esatta:');
disp(errore_relativo);

disp('Tempo (in secondi) per il calcolo della soluzione:')
disp(time)

if ispc() 
    % Se Windows
    disp('Memoria prima:')
    disp(start_memory.MemUsedMATLAB / 1e6)

    disp('Memoria dopo:')
    disp(final_memory.MemUsedMATLAB / 1e6)

    memory_diff = (final_memory.MemUsedMATLAB - start_memory.MemUsedMATLAB) / 1e6;

    disp('Differenza:')
    disp(memory_diff)
else
    % Se il sistema operativo è Linux
    [~, result] = system('free -b | grep Mem');
    memory_info = strsplit(result);
    memory_used = str2double(memory_info{3});
end