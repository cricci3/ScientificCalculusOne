package org.example;

import org.ejml.data.DMatrixSparseCSC;
import us.hebi.matlab.mat.ejml.Mat5Ejml;
import us.hebi.matlab.mat.format.Mat5;
import us.hebi.matlab.mat.types.Sparse;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class MatrixProcessor {
    private static final double SYMMETRY_TOLERANCE = 1e-8;
    private final Path matricesPath;

    public MatrixProcessor(Path matricesPath) {
        this.matricesPath = matricesPath;
    }

    public List<MatrixData> processMatrices() throws IOException {
        List<MatrixData> matrixDataList = new ArrayList<>();
        List<Path> matrixFiles = Files.list(matricesPath)
                .filter(Files::isRegularFile)
                .toList();

        for (Path file : matrixFiles) {
            System.out.println("Processing matrix: " + file.getFileName());
            try {
                MatrixData data = processMatrix(file);
                data.setStatus("Success");
                matrixDataList.add(data);
                System.out.println("Finished processing " + file.getFileName() + "\n");
            } catch (OutOfMemoryError e) {
                handleProcessingError(matrixDataList, file, "Error: Out of memory");
            } catch (Exception e) {
                handleProcessingError(matrixDataList, file, "Error: " + e.getMessage());
            }
        }

        return matrixDataList;
    }

    private MatrixData processMatrix(Path file) throws IOException {
        MatrixData data = new MatrixData();
        data.setMatrixName(file.getFileName().toString());
        data.setSize(Files.size(file));

        Sparse value = Mat5.readFromFile(file.toString())
                .getStruct("Problem")
                .getSparse("A");

        DMatrixSparseCSC A = Mat5Ejml.convert(value, new DMatrixSparseCSC(value.getNumRows(), value.getNumCols()));
        A.nz_length = value.getNumNonZero();
        MatrixSolver.validateMatrix(A, SYMMETRY_TOLERANCE);
        // Liberare la memoria non utilizzata
        System.gc();
        // Misura la memoria iniziale
        long startMemory = MemoryUtil.getUsedMemory();
        data.setMemoryUsed(startMemory);

        DMatrixSparseCSC B = MatrixSolver.createBVector(A);
        DMatrixSparseCSC x = new DMatrixSparseCSC(A.numRows, 1);

        long startTime = System.currentTimeMillis();
        MatrixSolver.solveSystem(A, B, x);
        data.setTime((System.currentTimeMillis() - startTime) / 1000.0);

        long endMemory = MemoryUtil.getUsedMemory();
        data.setMemoryUsed(endMemory - startMemory);

        data.setErroreRelativo(MatrixSolver.calculateRelativeError(x));

        return data;
    }

    private void handleProcessingError(List<MatrixData> matrixDataList, Path file, String errorMessage) {
        System.err.println(errorMessage + " while processing " + file.getFileName());
        MatrixData data = new MatrixData();
        data.setMatrixName(file.getFileName().toString());
        data.setStatus(errorMessage);
        matrixDataList.add(data);
    }
}
