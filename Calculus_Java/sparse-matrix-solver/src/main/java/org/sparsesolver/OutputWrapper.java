package org.sparsesolver;

import java.util.List;

public class OutputWrapper {
    private SystemInfo systemInfo;
    private List<MatrixData> matrixResults;

    public OutputWrapper(List<MatrixData> matrixResults) {
        this.systemInfo = new SystemInfo();
        this.matrixResults = matrixResults;
    }

    public SystemInfo getSystemInfo() { return systemInfo; }
    public void setSystemInfo(SystemInfo systemInfo) { this.systemInfo = systemInfo; }
    public List<MatrixData> getMatrixResults() { return matrixResults; }
    public void setMatrixResults(List<MatrixData> matrixResults) { this.matrixResults = matrixResults; }
}