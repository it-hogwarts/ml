from typing import List, Dict
import numpy as np


class Recommender():
    def __init__(self, source_path='source_files/'):
        with open(source_path + 'tech_matrix.npy', 'rb') as f:
            self.matrix = np.load(f)
        with open(source_path + 'skills.txt', 'r') as f:
            self.skills_list = [i.strip() for i in f.readlines()]
        self.comparator = {skill: i for i, skill in enumerate(self.skills_list)}
        self.skills_number = len(self.comparator)

    def search_candidates(self, tag: str):
        try:
            tag = self.comparator[tag.lower()]
        except:
            print('This tag ({}) is not in database'.format(tag))
            return {}
        candidates = {}
        for skill_ind in range(self.skills_number):
            if self.matrix[skill_ind][tag]:
                candidates[skill_ind] = self.matrix[skill_ind][tag]
        return candidates

    def merge_dicts(self, vocab1: Dict, vocab2: Dict) -> Dict:
        for key in vocab2:
            if key not in vocab1:
                vocab1[key] = 0
            vocab1[key] += vocab2[key]
        return vocab1

    def predict(self, tags_list: List[str], topk=3) -> List[str]:
        tags_list = [i.lower() for i in tags_list]
        candidates = {}
        for tag in tags_list:
            candidates = self.merge_dicts(candidates, self.search_candidates(tag))
        possibles_rated = sorted(list(candidates.keys()), key=lambda x: -candidates[x])
        rated_as_text = list(filter(lambda skill: skill not in tags_list,
                                    [self.skills_list[skill_ind] for skill_ind in possibles_rated]))
        return rated_as_text[:topk]


'''

USAGE EXAMPLE
recommendation_model = Recommender(source_path = 'C:/folder_for_files/')
print(recommendation_model.predict(['SQL', 'Python', 'Docker'], topk=5))

'''
