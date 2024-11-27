import numpy as np
import numpy.typing as npt
from typing import Dict, Any
from .distance_calculus.cosine_similarity import (
	cosine_similarity_vector_matrix
)

def sort_by_distances(
	user_embedding: npt.NDArray, 
	offers_embeddings: Dict[str, npt.NDArray]
) -> Dict[str, Any]: 
	"""Sort vectors by distances.
	
	:param user_embedding: ndaray: Embedding for the user.
	:param offers_embeddings: dict: Offers ids and their embedding

	return
		offer ids ordered by distance
	"""
	offers_ids = list(offers_embeddings.keys())
	offers_matrix = np.array(list(offers_embeddings.values()))

	cosine_sim_arr = np.zeros(len(offers_ids), dtype=float)
	cosine_similarity_vector_matrix(user_embedding, offers_matrix, cosine_sim_arr)

	top_similar = np.argsort(cosine_sim_arr)[::-1]
	top = [
		{
			"offer": offers_ids[i],
			"similarity": cosine_sim_arr[i],
		}
		for i in top_similar
	]
	
	return top
