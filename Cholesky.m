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
    % Calculate b
    b = matrix * xe;
    % Cholesky decomposition of matrix A
    R = chol(matrix);
    % Solve the system Ax = b
    % Solve for y in the lower triangular system R' * y = b
    y = R' \ b;
    % Solve for x in the upper triangular system R * x = y
    x = R \ y;
    time = toc;
    
    % Measure final memory
    final_memory = memoryFunc.memory;
    
    % Verify error
    errore_relativo = norm(x - xe, 2) / norm(xe, 2);
    
    % Calculate used memory
    memory_used = (final_memory - start_memory) / 1e6; % In MB
    
    % Save results in the structure
    results(i).File = matrixNames{i};
    results(i).Errore_Relativo = errore_relativo;
    results(i).Time = time;
    results(i).Memory_Used = memory_used;
    results(i).Status = 'Success';
    
    % Clear variables to free memory
    clear mtrx matrix x y R b
catch ME
    % If there's an error (e.g., out of memory), save relevant information
    results(i).File = matrixNames{i};
    results(i).Errore_Relativo = NaN;
    results(i).Time = NaN;
    results(i).Memory_Used = NaN;
    results(i).Status = ['Error: ', ME.message];
end

% Force garbage collection
pause(0.1);
java.lang.System.gc()
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
