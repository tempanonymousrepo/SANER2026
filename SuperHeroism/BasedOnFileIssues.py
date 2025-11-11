import time
import pickle as pkl
# import bson


class SuperHeroes:
    def __init__(self):
        self.hero_project_author_files = dict()
        self.hero_project_author_issues = dict()
        self.superhero_data = dict()

    def constructing_dictionaries(self):
        file_path = 'technicalHeroesFiles.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_files = pkl.load(file)
        print('dictionary 1 created')
        file_path = 'socialHeroesIssues.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_issues = pkl.load(file)
        print('dictionary 3 created')

    def constructing_final(self):
        for project in self.hero_project_author_files:
            if project in self.hero_project_author_issues:
                if project not in self.superhero_data:
                    self.superhero_data[project] = list()
                for author in self.hero_project_author_files[project]:
                    if author in self.hero_project_author_issues[project]:
                        self.superhero_data[project].append(author)
        for project in self.superhero_data:
            print(project)
            print(len(self.superhero_data[project]))
            print(len(self.hero_project_author_issues[project]))


if __name__ == "__main__":
    start_time = time.time()
    obj1 = SuperHeroes()
    obj1.constructing_dictionaries()
    obj1.constructing_final()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
