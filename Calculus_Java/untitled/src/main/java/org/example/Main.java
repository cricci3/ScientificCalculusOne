package org.example;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;

public class Main {
    private static final String MATRICES_PATH = "src/main/resources/Matrix";

    public static void main(String[] args) {
        try {
            MatrixProcessor processor = new MatrixProcessor(Paths.get(MATRICES_PATH));
            List<MatrixData> matrixDataList = processor.processMatrices();
            JSONWriter.writeJSON(matrixDataList);
        } catch (IOException e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}