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
        diff_memory = (final_memory - start_memory) / 1e6; % In MB

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

% Informazioni di sistema
system_info = struct('Language', 'MATLAB', 'Operating_System', computer);

% Risultati finali
final_results = struct('System_Info', system_info, 'Matrix_Results', results);

% Leggi il file JSON esistente
fid = fopen('results.json', 'r');
if fid == -1
    existing_data = struct();
else
    raw = fread(fid, inf, 'uint8=>char')';
    fclose(fid);
    existing_data = jsondecode(raw);
end

% Aggiungi i risultati di MATLAB mantenendo i dati esistenti
existing_data.Windows_MATLAB = final_results;


% Converti la struttura in JSON e salva nel file
jsonStr = jsonencode(existing_data);
fid = fopen('results.json', 'w');
if fid == -1
    error('Impossibile aprire il file per la scrittura.');
end
fwrite(fid, jsonStr, 'char');
fclose(fid);