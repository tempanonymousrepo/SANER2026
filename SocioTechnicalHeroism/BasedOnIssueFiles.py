import time
import pickle as pkl
# import bson


class SocioTechnicalHeroes:
    def __init__(self):
        self.project_author_number_of_files = dict()
        self.hero_project_author_issues = dict()
        self.socio_technical_commit_comment = dict()

    def constructing_dictionaries(self):
        file_path = 'project_author_number_of_files.pkl'
        with open(file_path, 'rb') as file:
            self.project_author_number_of_files = pkl.load(file)
        print('dictionary 1 created')
        file_path = 'socialHeroesIssues.pkl'
        with open(file_path, 'rb') as file:
            self.hero_project_author_issues = pkl.load(file)
        print('dictionary 3 created')

    def returning_median_authors_commits(self, project):
        num_authors = len(self.project_author_number_of_files[project])
        median_index = num_authors // 2
        l1 = list()
        for author in self.project_author_number_of_files[project]:
            l1.append(author)
        auth = l1[median_index]
        return self.project_author_number_of_files[project][auth]

    def extracting_socio_technical_commit_comment_heroes(self):
        for project in self.hero_project_author_issues:
            if project not in self.socio_technical_commit_comment:
                self.socio_technical_commit_comment[project] = list()
            for author in self.hero_project_author_issues[project]:
                if author in self.project_author_number_of_files[project]:
                    median_val = self.returning_median_authors_commits(project)
                    if self.project_author_number_of_files[project][author] >= median_val:
                        self.socio_technical_commit_comment[project].append(author)
        for project in self.socio_technical_commit_comment:
            print(project)
            print(len(self.socio_technical_commit_comment[project]))


if __name__ == "__main__":
    start_time = time.time()
    obj1 = SocioTechnicalHeroes()
    obj1.constructing_dictionaries()
    obj1.extracting_socio_technical_commit_comment_heroes()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
