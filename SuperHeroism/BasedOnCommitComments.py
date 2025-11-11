import time
import pickle as pkl
import bson
import matplotlib.pyplot as plt


class SuperHeroes:
    def __init__(self):
        self.hero_project_author_commits = dict()
        self.hero_project_author_comments = dict()
        self.superhero_data = dict()

    def constructing_dictionaries(self):
        file_path = 'technicalHeroesCommits.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_commits = pkl.load(file)
        file_path = 'technicalHeroesComments.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_comments = pkl.load(file)
    
    def constructing_final(self):
        for project in self.hero_project_author_commits:
            if project in self.hero_project_author_comments:
                if project not in self.superhero_data:
                    self.superhero_data[project] = list()
                for author in self.hero_project_author_commits[project]:
                    if author in self.hero_project_author_comments[project]:
                        self.superhero_data[project].append(author)

    def plotting(self):
        project_author_count = {project: len(authors) for project, authors in self.superhero_data.items()}
        project_names = list(project_author_count.keys())
        author_counts = list(project_author_count.values())
        plt.figure(figsize=(10, 6))
        plt.bar(project_names, author_counts, color='cyan')
        plt.xlabel("Project")
        plt.ylabel("Number of Heroes")
        plt.title("Superheroes based on commits and number of comments")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    start_time = time.time()
    obj1 = SuperHeroes()
    obj1.constructing_dictionaries()
    obj1.constructing_final()
    obj1.plotting()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
