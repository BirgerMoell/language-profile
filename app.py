import streamlit as st
import numpy as np
import scipy.stats as stats
from fpdf import FPDF
import base64
import os
from plots import test_profile
import matplotlib.pyplot as plt
from PIL import Image

# Function to calculate z-score
def calculate_z_score(test_score, mean, std_dev):
    return (test_score - mean) / std_dev

def z_score_calculator(value, norm_mean, norm_sd):
    z_value = (value - norm_mean) / norm_sd
    stanine_value = round(1.25 * z_value + 5.5)
    z_score = round(z_value, 2)
    return z_score, stanine_value

def bnt_calculator(age, education, bnt):
        if age <= 60 and education <= 12:
            norm_mean = 54.5
            norm_sd = 3.2
            z_score, stanine_value = z_score_calculator(bnt, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age <= 60 and education > 12:
            norm_mean = 54.0
            norm_sd = 4.4
            z_score, stanine_value = z_score_calculator(bnt, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age > 60 and education <= 12:
            norm_mean = 54.8
            norm_sd = 3.3
            z_score, stanine_value = z_score_calculator(bnt, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age > 60 and education > 12:
            norm_mean = 56.2
            norm_sd = 3.4
            z_score, stanine_value = z_score_calculator(bnt, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        else:
            print("missing value/ wrong format")

def fas_calculator(age, education, fas):
    if age <= 60 and education <= 12:
        norm_mean = 42.7
        norm_sd = 13.7
        z_score, stanine_value = z_score_calculator(fas, norm_mean, norm_sd)
        return norm_mean, norm_sd, z_score, stanine_value
    elif age <= 60 and education > 12:
        norm_mean = 46.7
        norm_sd = 13.7
        z_score, stanine_value = z_score_calculator(fas, norm_mean, norm_sd)
        return norm_mean, norm_sd, z_score, stanine_value
    elif age > 60 and education <= 12:
        norm_mean = 46.9
        norm_sd = 10.4
        z_score, stanine_value = z_score_calculator(fas, norm_mean, norm_sd)
        return norm_mean, norm_sd, z_score, stanine_value
    elif age > 60 and education > 12:
        norm_mean = 51.6
        norm_sd = 12.6
        z_score, stanine_value = z_score_calculator(fas, norm_mean, norm_sd)
        return norm_mean, norm_sd, z_score, stanine_value
    else:
        print("missing value/ wrong format")

def generate_graph(BNT_stanine, FAS_stanine):
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



def create_pdf(z_score, mean, std_dev, logo_path, plot_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font("Arial", size=12)

    # Add logos
    x_positions = [25, 85, 145]
    for i, logo_path in enumerate(logo_paths):
        pdf.image(logo_path, x=x_positions[i], y=8, w=40)
    pdf.set_xy(10, 50)


    # Add title and center it
    title = "Z-Score Report"
    pdf.set_font("Arial", style="B", size=16)
    title_width = pdf.get_string_width(title) + 6
    pdf.cell((210 - title_width) / 2)
    pdf.cell(title_width, 10, title, 0, 1, "C")

    # Add z-score and center it
    pdf.set_font("Arial", size=12)
    z_score_text = "Your z-score is: {:.2f}".format(z_score)
    z_score_width = pdf.get_string_width(z_score_text) + 6
    pdf.cell((210 - z_score_width) / 2)
    pdf.cell(z_score_width, 10, z_score_text, 0, 1, "C")

    # Add mean and standard deviation and center it
    mean_std_text = "Mean: {}, Standard Deviation: {}".format(mean, std_dev)
    mean_std_width = pdf.get_string_width(mean_std_text) + 6
    pdf.cell((210 - mean_std_width) / 2)
    pdf.cell(mean_std_width, 10, mean_std_text, 0, 1, "C")

    # Add logo
    pdf.image(plot_path, x=10, y=80, w=200)
    # pdf.set_xy(10, 40)

    # Add tool description and center it
    pdf.set_xy(10, 230)
    pdf.set_font("Arial", size=10)
    description = "This PDF report was generated using the Z-Score Calculator Streamlit App."
    pdf.multi_cell(0, 10, description, 0, "C")

     # Add explanatory text about the collaboration between KI and KTH
    pdf.set_xy(10, 255)
    pdf.set_font("Arial", size=8)
    collaboration_text = (
        "Den här PDF:en är en del av ett samarbetsprojekt mellan Karolinska Institutet (KI) och "
        "Kungliga Tekniska Högskolan (KTH) med målsättningen att använda artificiell intelligens (AI) och "
        "teknik för att minska administration i sjukhusarbete. Projektet fokuserar på att utveckla och "
        "implementera AI-baserade lösningar för att förbättra arbetsflöden, öka effektiviteten och "
        "minska den administrativa bördan för sjukvårdspersonal. För frågor om formuläret kontakta Fredrik Sand fredrik.sand-aronsson@regionstockholm.se, för frågor om teknik kontakta Birger Moëll bmoell@kth.se."
    )
    line_width = 190
    line_height = pdf.font_size_pt * 0.6
    lines = collaboration_text.split(' ')
    current_line = ''
    for word in lines:
        if pdf.get_string_width(current_line + word) < line_width:
            current_line += word + ' '
        else:
            pdf.cell(line_width, line_height, current_line, 0, 1)
            current_line = word + ' '
    pdf.cell(line_width, line_height, current_line, 0, 1)

    return pdf

def pdf_to_base64(pdf):
    with open(pdf, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')


# Title and description
st.title("Z-Score Calculator")
st.write("Enter your test score, age, and education level to calculate the z-score.")

# Input fields
#test_score = st.number_input("Test Score", min_value=0, value=0, step=1)
age = st.number_input("Age", min_value=0, value=18, step=1)
education_level = st.number_input("Education Level in years", min_value=0, value=18, step=1)
isw = st.number_input("ISW", min_value=0, value=0, step=1)
bnt = st.number_input("BNT", min_value=0, value=0, step=1)
fas = st.number_input("FAS", min_value=0, value=0, step=1)


# Calculate mean and standard deviation based on age and education level
# For simplicity, we will use made-up values for mean and std_dev
mean = np.random.randint(50, 100)
std_dev = np.random.randint(10, 30)

# Calculate z-score and display result
if st.button("Calculate Z-Score"):
    profile = test_profile(age, education_level, isw, bnt, fas)

    # for each value in the profile, calculate the z-score
    bnt_mean, bnt_std, z_bnt, stanine_bnt = bnt_calculator(age, education_level, bnt)
    fas_mean, fas_std, z_fas, stanine_fas = fas_calculator(age, education_level, fas)
    
    # z_score = calculate_z_score(test_score, mean, std_dev)
    st.write(f"Your bnt z-score is: {z_bnt:.2f}")
    st.write(f"Mean: {bnt_mean}, Standard Deviation: {bnt_std}")

    st.write(f"Your fas z-score is: {z_fas:.2f}")
    st.write(f"Mean: {fas_mean}, Standard Deviation: {fas_std}")
    # Create PDF
    # logo_path="logo.jpg"

    logo_paths = ["logo.jpg", "logo2.jpg", "logo3.jpg"]

    # create the plot from the dataframe

    # check if education level is more than 12 years, if more than 12, set value to one, otherwise zero
    education_level = 1 if education_level > 12 else 0

    plot_path = generate_graph(stanine_bnt, stanine_fas)

    # create an image from the plot and add to streamlit display
    image = Image.open(plot_path)
    st.image(image, caption='Stanine plot', use_column_width=True)

    pdf_filename = "z_score_report.pdf"
    pdf = create_pdf(z_bnt, bnt_mean, bnt_std, logo_paths, plot_path)
    pdf.output(name=pdf_filename)

    # Download PDF
    with open(pdf_filename, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_filename}">Download PDF</a>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Remove PDF file after download
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)