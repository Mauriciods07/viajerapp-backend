import numpy as np
import numba


@numba.guvectorize(
    ["void(float64[:], float64[:], float64[:])"], "(n),(n)->()"
)
def cosine_similarity_vector_matrix(u, v, result): 
	"""Calculate consine similarity from a vector and a matrix.
	
	:param u: ndarray: vector of dimension (1, n)
	:param v: ndarray: vector of dimension (n, m)
	:param result: ndarray: vector for return
	"""
	dim = u.shape[0]

	udotv = 0
	u_norm = 0
	v_norm = 0

	for i in range(dim):
		if (np.isnan(u[i])) or (np.isnan(v[i])):
			continue
		udotv += u[i]*v[i]
		u_norm += u[i]*u[i]
		v_norm += v[i]*v[i]

	cos_theta = 0
	if u_norm!=0 and v_norm!=0:
		cos_theta = udotv / np.sqrt(u_norm * v_norm)
	result[i] = cos_theta
