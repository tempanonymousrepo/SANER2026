import time
import pickle as pkl
# import bson
import matplotlib.pyplot as plt

class SuperHeroes:
    def __init__(self):
        self.hero_project_author_loc = dict()
        self.hero_project_author_issues = dict()
        self.superhero_data = dict()

    def constructing_dictionaries(self):
        file_path = 'technicalHeroesLOC.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_loc = pkl.load(file)
        print('dictionary 1 created')
        file_path = 'socialHeroesIssues.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_issues = pkl.load(file)
        print('dictionary 3 created')

    def constructing_final(self):
        for project in self.hero_project_author_loc:
            if project in self.hero_project_author_issues:
                if project not in self.superhero_data:
                    self.superhero_data[project] = list()
                for author in self.hero_project_author_loc[project]:
                    if author in self.hero_project_author_issues[project]:
                        self.superhero_data[project].append(author)
        for project in self.superhero_data:
            print(project)
            print(len(self.superhero_data[project]))
            # print(len(self.hero_project_author_issues[project]))

    def plotting(self):
        project_author_count = {project: len(authors) for project, authors in self.superhero_data.items()}

        # Extract project names and author counts for plotting
        project_names = list(project_author_count.keys())
        author_counts = list(project_author_count.values())

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(project_names, author_counts, color='orange')
        plt.xlabel("Project")
        plt.ylabel("Number of Heroes")
        plt.title("Superheroes based on lines of code and number of issues")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability

        # Display the plot
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
