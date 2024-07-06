package org.sparsesolver;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class Main {
    private static final String MATRICES_DIR = "Matrix"; // Specify relative directory

    public static void main(String[] args) {
        try {
            // Construct the path to the matrix directory
            Path matricesPath = Paths.get(MATRICES_DIR);

            MatrixProcessor processor = new MatrixProcessor(matricesPath);
            List<MatrixData> matrixDataList = processor.processMatrices();
            JSONWriter.writeJSON(matrixDataList);
        } catch (IOException e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
