package org.sparsesolver;

import org.ejml.data.DMatrixSparseCSC;
import us.hebi.matlab.mat.ejml.Mat5Ejml;
import us.hebi.matlab.mat.format.Mat5;
import us.hebi.matlab.mat.types.Sparse;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

public class MatrixProcessor {
    private static final Logger logger = Logger.getLogger(MatrixProcessor.class.getName());
    private static final double SYMMETRY_TOLERANCE = 1e-8;
    private final Path matricesPath;

    public MatrixProcessor(Path matricesPath) {
        this.matricesPath = matricesPath;
    }

    public List<MatrixData> processMatrices() throws IOException {
        List<MatrixData> matrixDataList = new ArrayList<>();
        try (var files = Files.list(matricesPath)) {
            files.filter(Files::isRegularFile)
                 .forEach(file -> matrixDataList.add(processMatrix(file)));
        }
        return matrixDataList;
    }

    private MatrixData processMatrix(Path file) {
        MatrixData data = new MatrixData();
        data.setMatrixName(file.getFileName().toString());
        try {
            data.setSize(Files.size(file));
            try (var mat5File = Mat5.readFromFile(file.toString())) {
                Sparse value = mat5File.getStruct("Problem").getSparse("A");
                DMatrixSparseCSC A = Mat5Ejml.convert(value, new DMatrixSparseCSC(value.getNumRows(), value.getNumCols()));
                A.nz_length = value.getNumNonZero();
                MatrixSolver.validateMatrix(A, SYMMETRY_TOLERANCE);
                long startMemory = MemoryUtil.getUsedMemory();
                data.setMemoryUsed(startMemory);
                DMatrixSparseCSC B = MatrixSolver.createBVector(A);
                DMatrixSparseCSC x = new DMatrixSparseCSC(A.numRows, 1);
                long startTime = System.nanoTime();
                MatrixSolver.solveSystem(A, B, x);
                data.setTime((System.nanoTime() - startTime) / 1e9);
                long endMemory = MemoryUtil.getUsedMemory();
                data.setMemoryUsed(endMemory - startMemory);
                data.setErroreRelativo(MatrixSolver.calculateRelativeError(x));
                data.setStatus("Success");
            }
        } catch (OutOfMemoryError e) {
            data.setStatus("Error: Out of memory");
        } catch (Exception e) {
            data.setStatus("Error: " + e.getMessage());
        }
        logger.info("Processed matrix: " + data.getMatrixName() + " - Status: " + data.getStatus());
        return data;
    }
}
