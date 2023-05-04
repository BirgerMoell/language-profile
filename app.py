import streamlit as st
import numpy as np
import scipy.stats as stats
from fpdf import FPDF
import base64
import os
from plots import test_profile
import matplotlib.pyplot as plt
from PIL import Image

test_dict = {
    "animal": {
        "low_age_low_education": {
            "mean": 21.0,
            "std": 7.0
        }, "low_age_high_education": {
            "mean": 22.4,
            "std": 6.8
        }, "high_age_low_education": {
            "mean": 22.1,
            "std": 5.7
        }, "high_age_high_education": {
            "mean": 25.6,
            "std": 5.6
        }
    }, "verb": {
        "low_age_low_education": {
            "mean": 17.6,
            "std": 4.3
        }, "low_age_high_education": {
            "mean": 20.5,
            "std": 5.4
        }, "high_age_low_education": {
            "mean": 16.7,
            "std": 6.1
        }, "high_age_high_education": {
            "mean": 22.7,
            "std": 5.1
        }
    },  "repetition": {
        "low_age_low_education": {
            "mean": 24.8,
            "std": 4.8
        }, "low_age_high_education": {
            "mean": 25.9,
            "std": 3.7
        }, "high_age_low_education": {
            "mean": 24.0,
            "std": 4.9
        }, "high_age_high_education": {
            "mean": 25.8,
            "std": 3.8
        }
    }, "months_backward": {
        "low_age_low_education": {
            "mean": 10.3,
            "std": 4.5
        }, "low_age_high_education": {
            "mean": 9.8,
            "std": 3.2
        }, "high_age_low_education": {
            "mean": 10.0,
            "std": 3.2
        }, "high_age_high_education": {
            "mean": 9.9,
            "std": 3.5
        }
    },
    "logicogrammatic": {
        "low_age_low_education": {
            "mean": 27.2,
            "std": 3.8
        }, "low_age_high_education": {
            "mean": 27.4,
            "std": 3.1
        }, "high_age_low_education": {
            "mean": 23.5,
            "std": 4.2
        }, "high_age_high_education": {
            "mean": 27.2,
            "std": 3.3
        }
    },"inference": {
        "low_age_low_education": {
            "mean": 28.2,
            "std": 2.4
        }, "low_age_high_education": {
            "mean": 28.4,
            "std": 2.8
        }, "high_age_low_education": {
            "mean": 25.2,
            "std": 3.9
        }, "high_age_high_education": {
            "mean": 27.3,
            "std": 2.9
        }
    }, "reading_speed": {
        "low_age_low_education": {
            "mean": 21.5,
            "std": 5.4
        }, "low_age_high_education": {
            "mean": 27.3,
            "std": 5.5
        }, "high_age_low_education": {
            "mean": 23.0,
            "std": 7.2
        }, "high_age_high_education": {
            "mean": 28.8,
            "std": 5.2
        }
    }, "decoding_words": {
        "low_age_low_education": {
            "mean": 107.6,
            "std": 27.8
        }, "low_age_high_education": {
            "mean": 112.9,
            "std": 22.7
        }, "high_age_low_education": {
            "mean": 111.4,
            "std": 26.1
        }, "high_age_high_education": {
            "mean": 122.9,
            "std": 28.2
        }
    }, "decoding_non_words": {
        "low_age_low_education": {
            "mean": 95.8,
            "std": 26.6
        }, "low_age_high_education": {
            "mean": 105.4,
            "std": 29.5
        }, "high_age_low_education": {
            "mean": 103.4,
            "std": 25.2
        }, "high_age_high_education": {
            "mean": 118.0,
            "std": 26.8
        }
    },
    # jönsson och winnerstam 2012
    "pataka": {
        "low_age_low_education": {
            "mean": 5.8,
            "std": 1.0
        }, "low_age_high_education": {
             "mean": 5.8,
            "std": 1.0
        }, "high_age_low_education": {
             "mean": 5.8,
            "std": 1.0
        }, "high_age_high_education": {
            "mean": 5.8,
            "std": 1.0
        }
    }
}


# Function to calculate z-score
def calculate_z_score(test_score, mean, std_dev):
    return (test_score - mean) / std_dev

def z_score_calculator(value, norm_mean, norm_sd):
    z_value = (value - norm_mean) / norm_sd
    stanine_value = round(1.25 * z_value + 5.5)
    z_score = round(z_value, 2)
    return z_score, stanine_value

def test_calculator(age, education, values, test):
        if age <= 60 and education <= 12:
            norm_mean = test_dict[test]["low_age_low_education"]["mean"]
            norm_sd = test_dict[test]["low_age_low_education"]["std"]
            z_score, stanine_value = z_score_calculator(values, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age <= 60 and education > 12:
            norm_mean = test_dict[test]["low_age_high_education"]["mean"]
            norm_sd = test_dict[test]["low_age_high_education"]["std"]
            z_score, stanine_value = z_score_calculator(values, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age > 60 and education <= 12:
            norm_mean = test_dict[test]["high_age_low_education"]["mean"]
            norm_sd = test_dict[test]["high_age_low_education"]["std"]
            z_score, stanine_value = z_score_calculator(values, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        elif age > 60 and education > 12:
            norm_mean = test_dict[test]["high_age_high_education"]["mean"]
            norm_sd = test_dict[test]["high_age_high_education"]["std"]
            z_score, stanine_value = z_score_calculator(values, norm_mean, norm_sd)
            return norm_mean, norm_sd, z_score, stanine_value
        else:
            print("missing value/ wrong format")


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

def generate_graph(test_dict):
    # Create a plot
    fig, ax = plt.subplots()

    # Adjust the margins to fix the labels being cut off
    fig.subplots_adjust(left=0.25)

    # Set axis labels and title
    ax.set_xlabel('Stanine values')
    ax.set_ylabel('Test')

    # Set the x-axis to display the stanine values
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

    # Set the y-axis to display the tests
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    # Set the test labels to the keys in test_dict (in reverse order)
    ax.set_yticklabels(reversed(list(test_dict.keys())))

    # Set the range of the x-axis
    ax.set_xlim([0, 10])

    i = 1

    for test in reversed(list(test_dict.keys())):
        #print("the test is", test)
        ax.scatter(test_dict[test][4], i, s=50, color='black', label=test)
        i = i + 1

    # Save the graph as a png file
    fig.savefig('test_profile.png')
    return 'test_profile.png'


def create_pdf(test_dict, logo_path, plot_path):
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
    title = "Patient Summary"
    pdf.set_font("Times", style="B", size=12)
    title_width = pdf.get_string_width(title) + 6
    pdf.cell((210 - title_width) / 2)
    pdf.cell(title_width, 10, title, 0, 1, "C")

    # Add z-score and center it

    pdf.set_font("Times", size=12)

    tests_per_line = 1
    tests_count = len(test_dict)
    line_count = tests_count // tests_per_line + (1 if tests_count % tests_per_line > 0 else 0)

    test_index = 0
    left_margin = 15
    col_width = (210 - 2 * left_margin) / tests_per_line

    for line in range(line_count):
        pdf.set_x(left_margin)
        for test in list(test_dict.keys())[test_index:test_index + tests_per_line]:
            # Set the font to bold for the test value
            pdf.set_font("Arial", style="B", size=8)
            test_text = "{}: ".format(test)
            test_width = pdf.get_string_width(test_text)
            pdf.cell(test_width, 6, test_text, 0, 0, "C")  # Changed the line height to 6

            # Set the font to normal for the rest of the text
            pdf.set_font("Arial", size=8)
            z_score_text = "{:.2f} (Mean: {:.2f}, Std: {:.2f})".format(
                test_dict[test][3], test_dict[test][1], test_dict[test][2]
            )
            z_score_width = pdf.get_string_width(z_score_text) + 2  # Reduced the additional width to 2
            pdf.cell((210 / tests_per_line - test_width - z_score_width) / 2)
            pdf.cell(z_score_width, 6, z_score_text, 0, 0, "C")  # Changed the line height to 6

            test_index += 1
        pdf.ln(12)  # Reduced the line spacing to 12

    # Add logo
    pdf.add_page()

    pdf.image(plot_path, x=10, y=20, w=200)
    # pdf.set_xy(10, 40)

    # Add tool description and center it
    pdf.set_xy(10, 200)
    pdf.set_font("Arial", size=10)
    description = "This PDF report was generated using the Patient Summary App."
    pdf.multi_cell(0, 10, description, 0, "C")

     # Add explanatory text about the collaboration between KI and KTH
    pdf.set_xy(10, 220)
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
st.title("Language profile")
st.write("Enter your test score, to calculate scores and create a PDF with the results.")

# Input fields
#test_score = st.number_input("Test Score", min_value=0, value=0, step=1)
age = st.number_input("Age", min_value=0, value=18, step=1)
education_level = st.number_input("Education Level in years", min_value=0, value=18, step=1)
isw = st.number_input("ISW", min_value=0.0, value=0.0, step=0.01)
bnt = st.number_input("BNT", min_value=0, value=0, step=1)
fas = st.number_input("FAS", min_value=0, value=0, step=1)
animal = st.number_input("Animal", min_value=0, value=0, step=1)
verb = st.number_input("Verb", min_value=0, value=0, step=1)
repetition = st.number_input("Repetition", min_value=0, value=0, step=1)
logicogrammatic = st.number_input("Logicogrammatic", min_value=0, value=0, step=1)
inference = st.number_input("Inference", min_value=0, value=0, step=1)
reading_speed = st.number_input("Reading Speed", min_value=0, value=0, step=1)
decoding_words = st.number_input("Decoding Words", min_value=0.0, value=0.0, step=0.01)
decoding_non_words = st.number_input("Decoding Non-Words", min_value=0.0, value=0.0, step=0.01)
months_backward = st.number_input("Months Backward", min_value=0.0, value=0.0, step=0.01)
pataka = st.number_input("Pataka", min_value=0.0, value=0.0, step=0.01)


# add all the tests


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
    
    animal_mean, animal_std, animal_z, animal_stanine = test_calculator(age, education_level, animal, "animal")
    verb_mean, verb_std, verb_z, verb_stanine = test_calculator(age, education_level, verb, "verb")
    repetition_mean, repetition_std, repetition_z, repetition_stanine = test_calculator(age, education_level, repetition, "repetition")
    months_backward_mean, months_backward_std, months_backward_z, months_backward_stanine = test_calculator(age, education_level, months_backward, "months_backward")
    logicogrammatic_mean, logicogrammatic_std, logicogrammatic_z, logicogrammatic_stanine = test_calculator(age, education_level, logicogrammatic, "logicogrammatic")
    inference_mean, inference_std, inference_z, inference_stanine = test_calculator(age, education_level, inference, "inference")
    reading_speed_mean, reading_speed_std, reading_speed_z, reading_speed_stanine = test_calculator(age, education_level, reading_speed, "reading_speed")
    decoding_words_mean, decoding_words_std, decoding_words_z, decoding_words_stanine = test_calculator(age, education_level, decoding_words, "decoding_words")
    decoding_non_words_mean, decoding_non_words_std, decoding_non_words_z, decoding_non_words_stanine = test_calculator(age, education_level, decoding_non_words, "decoding_non_words")
    pataka_mean, pataka_std, pataka_z, pataka_stanine = test_calculator(age, education_level, pataka, "pataka")

    ## add all the tests with their values to an array

    ## CREATA A DICTORINARY WITH ALL THE TESTS AND THEIR Z-SCORES AND STANINE VALUES
    test_dict = {
        "bnt": [bnt, bnt_mean, bnt_std, z_bnt, stanine_bnt],
        "fas": [fas, fas_mean, fas_std, z_fas, stanine_fas],
        "animal": [animal, animal_mean, animal_std, animal_z, animal_stanine],
        "verb": [verb, verb_mean, verb_std, verb_z, verb_stanine],
        "repetition": [repetition, repetition_mean, repetition_std, repetition_z, repetition_stanine],
        "months_backward": [months_backward, months_backward_mean, months_backward_std, months_backward_z, months_backward_stanine],
        "logicogrammatic": [logicogrammatic, logicogrammatic_mean, logicogrammatic_std, logicogrammatic_z, logicogrammatic_stanine],
        "inference": [inference, inference_mean, inference_std, inference_z, inference_stanine],
        "reading_speed": [reading_speed, reading_speed_mean, reading_speed_std, reading_speed_z, reading_speed_stanine],
        "decoding_words": [decoding_words, decoding_words_mean, decoding_words_std, decoding_words_z, decoding_words_stanine],
        "decoding_non_words": [decoding_non_words, decoding_non_words_mean, decoding_non_words_std, decoding_non_words_z, decoding_non_words_stanine],
        "pataka": [pataka, pataka_mean, pataka_std, pataka_z, pataka_stanine]
    }

    # z_values = [z_bnt, z_fas, animal_z, verb_z, repetition_z, months_backward_z, logicogrammatic_z, inference_z, reading_speed_z, decoding_words_z, decoding_non_words_z, pataka_z]
    
    # ## add all the stanines to a list
    # stanine_values = [stanine_bnt, stanine_fas, animal_stanine, verb_stanine, repetition_stanine, months_backward_stanine, logicogrammatic_stanine, inference_stanine, reading_speed_stanine, decoding_words_stanine, decoding_non_words_stanine, pataka_stanine]

    # loop over and write out all the z values

    # loop over all the values in test dict and print out the z-score, mean and std_dev and stanine
    for key, value in test_dict.items():
        st.write(f"Your {key} z-score is: {value[3]:.2f}")
        st.write(f"Mean: {value[1]}, Standard Deviation: {value[2]}")
        st.write(f"Stanine: {value[4]}")

    # Create PDF

    logo_paths = ["logo.jpg", "logo2.jpg", "logo3.jpg"]

    # create the plot from the dataframe

    # check if education level is more than 12 years, if more than 12, set value to one, otherwise zero

    plot_path = generate_graph(test_dict)

    # create an image from the plot and add to streamlit display
    image = Image.open(plot_path)
    st.image(image, caption='Stanine plot', use_column_width=True)

    pdf_filename = "z_score_report.pdf"
    pdf = create_pdf(test_dict, logo_paths, plot_path)
    pdf.output(name=pdf_filename)

    # Download PDF
    with open(pdf_filename, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_filename}">Download PDF</a>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Remove PDF file after download
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)