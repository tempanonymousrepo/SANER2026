import time
import pickle as pkl
# import bson
import matplotlib.pyplot as plt


class TechnoSocialHeroes:
    def __init__(self):
        self.project_author_number_of_comments = dict()
        self.hero_project_author_loc = dict()
        self.techno_social_commit_comment = dict()

    def constructing_dictionaries(self):
        file_path = 'project_author_number_of_comments.pkl'
        with open(file_path, 'rb') as file:
            self.project_author_number_of_comments = pkl.load(file)
        print('dictionary 1 created')
        file_path = 'technicalHeroesLOC.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_loc = pkl.load(file)
        print('dictionary 3 created')

    def returning_median_authors_commits(self, project):
        num_authors = len(self.project_author_number_of_comments[project])
        median_index = num_authors // 2
        l1 = list()
        for author in self.project_author_number_of_comments[project]:
            l1.append(author)
        auth = l1[median_index]
        return self.project_author_number_of_comments[project][auth]

    def extracting_socio_technical_commit_comment_heroes(self):
        for project in self.hero_project_author_loc:
            if project not in self.techno_social_commit_comment:
                self.techno_social_commit_comment[project] = list()
            for author in self.hero_project_author_loc[project]:
                if author in self.project_author_number_of_comments[project]:
                    median_val = self.returning_median_authors_commits(project)
                    if self.project_author_number_of_comments[project][author] >= median_val:
                        self.techno_social_commit_comment[project].append(author)
        for project in self.techno_social_commit_comment:
            print(project)
            print(len(self.techno_social_commit_comment[project]))

    def plotting(self):
        project_author_count = {project: len(authors) for project, authors in self.techno_social_commit_comment.items()}

        # Extract project names and author counts for plotting
        project_names = list(project_author_count.keys())
        author_counts = list(project_author_count.values())

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(project_names, author_counts, color='green')
        plt.xlabel("Project")
        plt.ylabel("Number of Heroes")
        plt.title("Techno-social heroes based on lines of code and number of comments")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability

        # Display the plot
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    start_time = time.time()
    obj1 = TechnoSocialHeroes()
    obj1.constructing_dictionaries()
    obj1.extracting_socio_technical_commit_comment_heroes()
    obj1.plotting()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
