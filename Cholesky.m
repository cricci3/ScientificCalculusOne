% Usa la classe OSmemory per la misurazione della memoria
memoryFunc = OSmemory;

matrixNames = {'apache2.mat', 'cfd1.mat', 'cfd2.mat', 'ex15.mat', 'Flan_1565.mat', 'G3_circuit.mat', 'parabolic_fem.mat', 'shallow_water1.mat', 'StocF-1465.mat'};

% Inizializza una struttura per memorizzare i risultati
results = struct('File', {}, 'N', {}, 'Errore_Relativo', {}, 'Time', {}, 'Memory_Used', {}, 'Status', {});

for i = 1:length(matrixNames)
    % Usa fullfile per creare percorsi file indipendenti dal sistema operativo
    mtrx = load(fullfile(script_path, 'Matrix', matrixNames{i}));
    start_memory = memoryFunc.memory();
    disp(['Memoria iniziale per ', matrixNames{i}, ': ', num2str(start_memory)]);
    matrix = mtrx.Problem.A;

    % Creazione del vettore xe
    n = size(matrix, 1);
    xe = ones(n, 1);

    try
        tic;
        % Calcola b
        b = matrix * xe;
        % Decomposizione di Cholesky della matrice A
        R = chol(matrix);
        % Risolvi il sistema Ax = b
        % Risolvi per y nel sistema triangolare inferiore R' * y = b
        y = R' \ b;
        % Risolvi per x nel sistema triangolare superiore R * x = y
        x = R \ y;
        time = toc;

        % Misura la memoria finale
        final_memory = memoryFunc.memory();
        disp(['Memoria finale per ', matrixNames{i}, ': ', num2str(final_memory)]);

        % Calcola la memoria utilizzata
        memory_used = (final_memory - start_memory) / 1e6; % In MB

        % Controllo e gestione della memoria negativa
        if memory_used < 0
            % Se la memoria è negativa, aspetta un momento e ricontrolla
            pause(1);
            final_memory = memoryFunc.memory();
            memory_used = (final_memory - start_memory) / 1e6; % In MB

            % Se è ancora negativa, segna come errore
            if memory_used < 0
                error(['Memoria negativa rilevata per ', matrixNames{i}]);
            end
        end

        % Verifica l'errore
        errore_relativo = norm(x - xe, 2) / norm(xe, 2);

        % Salva i risultati nella struttura
        results(i).File = matrixNames{i};
        results(i).N = n;
        results(i).Errore_Relativo = errore_relativo;
        results(i).Time = time;
        results(i).Memory_Used = memory_used;
        results(i).Status = 'Success';

        % Pulisci le variabili per liberare memoria
        clear mtrx matrix x y R b
    catch ME
        % Se c'è un errore (es. memoria esaurita), salva le informazioni rilevanti
        results(i).File = matrixNames{i};
        results(i).N = n;
        results(i).Errore_Relativo = NaN;
        results(i).Time = NaN;
        results(i).Memory_Used = NaN;
        results(i).Status = ['Error: ', ME.message];
    end

    % Forza la garbage collection
    pause(0.1);
    java.lang.System.gc()
end

% Informazioni di sistema
system_info = struct('Language', 'MATLAB', 'Operating_System', computer);

% Risultati finali
final_results = struct('System_Info', system_info, 'Matrix_Results', results);

% Leggi il file JSON esistente
json_file = fullfile(script_path, 'results.json');
if exist(json_file, 'file')
    fid = fopen(json_file, 'r');
    raw = fread(fid, inf, 'uint8=>char')';
    fclose(fid);
    existing_data = jsondecode(raw);
else
    existing_data = struct();
end

% Aggiungi i risultati di MATLAB mantenendo i dati esistenti
if ispc
    existing_data.Windows_MATLAB = final_results;
else
    existing_data.Linux_MATLAB = final_results;
end

% Converti la struttura in JSON e salva nel file
jsonStr = jsonencode(existing_data);
fid = fopen(json_file, 'w');
if fid == -1
    error('Impossibile aprire il file per la scrittura.');
end
fwrite(fid, jsonStr, 'char');
fclose(fid);
