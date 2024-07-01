package org.example;

public class MatrixData {
    private String matrixName;
    private long size;
    private long memoryUsed;
    private double time;
    private double erroreRelativo;
    private String status;

    // Getters and setters
    public String getMatrixName() { return matrixName; }
    public void setMatrixName(String matrixName) { this.matrixName = matrixName; }
    public long getSize() { return size; }
    public void setSize(long size) { this.size = size; }
    public long getMemoryUsed() { return memoryUsed; }
    public void setMemoryUsed(long memoryUsed) { this.memoryUsed = memoryUsed; }
    public double getTime() { return time; }
    public void setTime(double time) { this.time = time; }
    public double getErroreRelativo() { return erroreRelativo; }
    public void setErroreRelativo(double erroreRelativo) { this.erroreRelativo = erroreRelativo; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}