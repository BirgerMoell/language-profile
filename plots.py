import matplotlib.pyplot as plt

class test_profile:
    def __init__(self, age, education, bnt, fas, isw):
        self.age = age
        self.education = education
        self.bnt = bnt
        self.fas = fas
        self.isw = isw
    
    def mean_bnt(self):
        if self.age <= 60 and self.education <= 12:
            self.norm_mean = 54.5
            self.norm_sd = 3.2
        elif self.age <= 60 and self.education > 12:
            self.norm_mean = 54.0
            self.norm_sd = 4.4
        elif self.age > 60 and self.education <= 12:
            self.norm_mean = 54.8
            self.norm_sd = 3.3
        elif self.age > 60 and self.education > 12:
            self.norm_mean = 56.2
            self.norm_sd = 3.4
        else:
            print("missing value/ wrong format")
    
    def z_bnt(self):
        self.mean_bnt()
        z_bnt = (self.bnt - self.norm_mean) / self.norm_sd
        stanine_bnt = round(1.25 * z_bnt + 5.5)
        return round(z_bnt, 2), stanine_bnt
    
    def z_to_stanine(self, z_score):
        stanine = round(1.25 * z_score + 5.5)
        return stanine


    def mean_fas(self):
        if self.age <= 60 and self.education <= 12:
            self.norm_mean = 42.7
            self.norm_sd = 13.7
        elif self.age <= 60 and self.education > 12:
            self.norm_mean = 46.7
            self.norm_sd = 13.7
        elif self.age > 60 and self.education <= 12:
            self.norm_mean = 46.9
            self.norm_sd = 10.4
        elif self.age > 60 and self.education > 12:
            self.norm_mean = 51.6
            self.norm_sd = 12.6
        else:
            print("missing value/ wrong format")
    

    def z_fas(self):
        self.mean_fas()
        z_fas = (self.fas - self.norm_mean) / self.norm_sd
        stanine_fas = round(1.25 * z_fas + 5.5)
        return round(z_fas, 2), stanine_fas


    def calculate_isw(self):
        isw_score = 74.38 + self.isw*0.66 - self.age*0.20 + self.education*1.77
        return round(isw_score, 2)

    def generate_graph(self):
        BNT_z, _ = self.z_bnt()
        FAS_z, _ = self.z_fas()

        BNT_stanine = self.z_to_stanine(BNT_z)
        FAS_stanine = self.z_to_stanine(FAS_z)

        # Create a plot
        fig, ax = plt.subplots()

        # Set axis labels and title
        ax.set_xlabel('Stanine values')
        ax.set_ylabel('Test')

        # Set the y-axis to display the tests
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['BNT', 'FAS'])

        # Set the range of the x-axis
        ax.set_xlim([0, 10])

        # Add dots for BNT and FAS scores
        ax.scatter(BNT_stanine, 1, s=100, label='BNT')
        ax.scatter(FAS_stanine, 2, s=100, label='FAS')

        # Add legend
        ax.legend()

        # Show the plot
        # plt.show()

        # Save the graph as a png file
        fig.savefig('test_profile.png')
        return 'test_profile.png'

