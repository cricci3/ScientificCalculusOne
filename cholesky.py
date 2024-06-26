import scipy.io
import numpy as np
from scipy.linalg import cholesky, LinAlgError
import scipy.sparse.linalg as spla


#  Matrix should be symmetric and positive definite
#  Definita positiva se
#       tutti autovalori > 0
#       elementi su diagonale > 0


def is_symmetric(matrix):
    return np.all(matrix.data == matrix.transpose().data)


#  def is_positive_definite(matrix):
#      return np.all(np.linalg.eigvals(matrix.toarray())) > 0 and np.all(np.diag(matrix)) > 0

def is_positive_definite(matrix):
    try:
        eigenvalue, _ = spla.eigsh(matrix, k=1, which='LM')
        return np.all(matrix.diagonal() > 0) and eigenvalue > 0
    except spla.ArpackNoConvergence:
        return False


# Load the .mat file
data = scipy.io.loadmat('Matrix/cfd1.mat')

# Stampare le chiavi per esaminare la struttura del dizionario
print(data.keys())

A = data['Problem'][0, 0]['A']
A = scipy.sparse.csr_matrix(A)

# Verifica se la matrice è simmetrica
if is_symmetric(A):
    print("La matrice è simmetrica.")
else:
    print("La matrice non è simmetrica.")

# Verifica se la matrice è definita positiva
if is_positive_definite(A):
    print("La matrice è definita positiva.")
else:
    print("La matrice non è definita positiva.")

