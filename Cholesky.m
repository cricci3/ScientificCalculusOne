import OSmemory.memory;

memoryFunc = OSmemory;

matrixNames = {'apache2.mat', 'cfd1.mat', 'cfd2.mat', 'ex15.mat','Flan_1565.mat', 'G3_circuit.mat','parabolic_fem.mat','shallow_water1.mat', 'StocF-1465.mat'};

% Inizializza una cella per memorizzare i risultati
results = struct('File', {}, 'Errore_Relativo', {}, 'Time', {}, 'Memory_Used', {}, 'Status', {});

for i = 1:length(matrixNames)
    mtrx = load(['Matrix/', matrixNames{i}]);
    start_memory = memoryFunc.memory;
    matrix = mtrx.Problem.A;
    
    % Creazione del vettore xe
    n = size(matrix, 1);  % Dimensione della matrice
    xe = ones(n, 1);
    
    try
        tic;
        
        % Calcolo del termine noto b
        b = matrix * xe;
        
        % Decomposizione di Cholesky della matrice A
        R = chol(matrix);
        
        % Risoluzione del sistema Ax = b
        % Risolviamo per y nel sistema triangolare inferiore R' * y = b
        y = R' \ b;
        
        % Risolviamo per x nel sistema triangolare superiore R * x = y
        x = R \ y;
        
        time = toc;
        final_memory = memoryFunc.memory;
        
        % Verifica dell'errore
        errore_relativo = norm(x - xe, 2) / norm(xe, 2);

        % Calcolo della memoria utilizzata
        diff_memory = (final_memory - start_memory) / 1e3; % In kB

        % Salva i risultati nella struttura
        results(i).File = matrixNames{i};
        results(i).Errore_Relativo = errore_relativo;
        results(i).Time = time;
        results(i).Memory_Used = diff_memory;
        results(i).Status = 'Success';
    catch ME
        % Se c'è un errore (es. out of memory), salva le informazioni rilevanti
        results(i).File = matrixNames{i};
        results(i).Errore_Relativo = NaN;
        results(i).Time = NaN;
        results(i).Memory_Used = NaN;
        results(i).Status = ['Error: ', ME.message];
    end
end

% Converti la struttura in JSON e salva nel file
jsonStr = jsonencode(results);
fid = fopen('results_Matlab.json', 'w');
if fid == -1
    error('Impossibile aprire il file per la scrittura.');
end
fwrite(fid, jsonStr, 'char');
fclose(fid);
