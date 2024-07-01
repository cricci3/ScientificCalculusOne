package org.example;

import org.ejml.data.DMatrixRMaj;
import org.ejml.data.DMatrixSparseCSC;
import org.ejml.interfaces.linsol.LinearSolverSparse;
import org.ejml.sparse.FillReducing;
import org.ejml.sparse.csc.CommonOps_DSCC;
import org.ejml.sparse.csc.CommonOps_MT_DSCC;
import org.ejml.sparse.csc.MatrixFeatures_DSCC;
import org.ejml.sparse.csc.NormOps_DSCC;
import org.ejml.sparse.csc.factory.LinearSolverFactory_DSCC;

public class MatrixSolver {

    public static void validateMatrix(DMatrixSparseCSC A, double symmetryTolerance) {
       if (!MatrixFeatures_DSCC.isPositiveDefinite(A)) {
          throw new IllegalArgumentException("Matrix is not positive definite");
       }
        if (!MatrixFeatures_DSCC.isSymmetric(A, symmetryTolerance)) {
            throw new IllegalArgumentException("Matrix is not symmetric");
        }
    }

    public static DMatrixSparseCSC createBVector(DMatrixSparseCSC A) {
        DMatrixSparseCSC tmp = new DMatrixSparseCSC(A.numRows, 1);
        CommonOps_DSCC.fill(tmp, 1);
        return CommonOps_MT_DSCC.mult(A, tmp, null);
    }

    public static void solveSystem(DMatrixSparseCSC A, DMatrixSparseCSC B, DMatrixSparseCSC x) {
        LinearSolverSparse<DMatrixSparseCSC, DMatrixRMaj> solver = LinearSolverFactory_DSCC.cholesky(FillReducing.NONE);
        solver.setA(A);
        solver.solveSparse(B, x);
    }

    public static double calculateRelativeError(DMatrixSparseCSC x) {
        DMatrixSparseCSC xe = new DMatrixSparseCSC(x.numRows, 1);
        CommonOps_DSCC.fill(xe, 1);
        DMatrixSparseCSC diff = new DMatrixSparseCSC(x.numRows, x.numCols);

        for (int i = 0; i < x.numRows; i++) {
            for (int j = 0; j < x.numCols; j++) {
                double valueX = x.get(i, j);
                double valueXe = xe.get(i, j);
                double result = valueX - valueXe;
                if (result != 0) {
                    diff.set(i, j, result);
                }
            }
        }

        double normDiff = NormOps_DSCC.normF(diff);
        double normXe = NormOps_DSCC.normF(xe);

        return normDiff / normXe;
    }
}