# About the package

PyGLA, or the Python Group Learning Assessment, is a library package designed to facilitate group-based learning and assess the individual contributions within a group. This approach is based on the findings presented in the paper "The Evolution of a Peer Assessment Method for use in Group-based Teaching of HCI," which provides in-depth information about the concept and its implementation.

# How to use the package?
 You can either
 
- To install the latest stable version of MNE-Python, you can use pip in a terminal:

  `pip install pygla`
- Get the latest code
`pip install -U https://github.com/balandongiv/pygla.git`

# Significant

The pygla system is a python-based implementation of the "The Evolution of a Peer Assessment Method for use in Group based Teaching of HCI." pygla stands for Pythonic-Based Group Learning Assessment. This new system serves as an upgrade from the previous Microsoft architecture-based implementation. The previous implementation was limited in several ways. Firstly, manual data entry of each entry from the Microsoft Word form into the excel template was time-consuming and complex. This manual approach was also prone to human error and limited to domain experts. With new teaching assistants every semester, the module convener had to constantly conduct or explain the procedure multiple times.

pygla addresses these limitations with the goal of automating the entire process. While the system does require some coding skills, the requirements are minimal. The Python library is capable of receiving peer assessment inputs conducted using Microsoft Forms and also supports manual data entry for peer assessments collected using Microsoft Word.

In addition, pygla is also capable of utilizing both the ‘five-point’ and ‘seven-point’ scales and theoretically the “ten-point” scale. This flexibility allows the module convener to choose the scale that best suits their needs and requirements. For instance, the module convener may choose to experiment with different scales to see the impact on marking.

In addition to that, the Excel implementation lacks the ability to capture and display the students' justifications for each criterion to their fellow members. These justifications or feedback play a crucial role in the assessment process as they provide insight for the module convener to determine the acceptability of the ratings assigned to each student-fellow pair. Furthermore, by capturing and sharing these justifications and feedback, students can use this information for self-improvement or as a means of recognizing and acknowledging their peers' good work. pygla also includes the important feature of anonymizing the name of the person providing the feedback, which promotes fairness and helps to eliminate bias in the evaluation process.
# Create peer assessment using Microsoft Forms

- Section "Group Details":
  - Student ID: This is the registered university student ID that is usually used to tie to the student's mark.
  - Group Name: This is the input about the student's assigned group. Pygla only accepts group names in an integer format (e.g. 1, 2, 3, etc.).
- Section "Peer":
  - Peer Name: This is the name of the fellow group member being rated.
  - Peer Student ID: This is the registered university student ID of the fellow group member being rated.
  - Assessment Components: This section includes the following criteria for peer assessment:
    - Research & Information gathering
    - Creative input
    - Co-operation within group
    - Communication within group
    - Quality of individual contributions
    - Attendance at meetings
  - Justification for Peer: Students are encouraged to justify their ratings for each peer assessment criterion.
  - Do you want to evaluate the next peer? This button is a branching function in Microsoft Forms to move to the next page, which would be a new fellow member to be rated.

Remarks:

- The content of the "Peer" section can be duplicated multiple times.

It is recommended to have more than 7 unique "Peer" sections to accommodate large groups. It is essential to use numbering nomenclature to allow pygla to know which input is for which section. For example, two "Peer" sections could look like this: "Peer 1" and "Peer 2".

## Peer 1
![Calendar

Description automatically generated with low confidence](Aspose.Words.f1fa9c9f-c409-43c6-aa03-336be62956d9.001.png)


## Peer 2

![Calendar

Description automatically generated](Aspose.Words.f1fa9c9f-c409-43c6-aa03-336be62956d9.002.png)

## Template
To simplify the process, a template for the "7-scales" peer assessment form is available for duplication through the following links. 

<https://forms.office.com/Pages/ShareFormPage.aspx?id=2hNDJ-EYq0CX4K3G6x7GmbYwOb71ABBOo9w744JCRipUMzVKSU5LUDlNSFRQWUMzQkhHMUk3UTdVWi4u&sharetoken=A2K3g1L1d4UzQ3PQpBth>

Simply access the links, duplicate the template, and customize it to suit your needs. With this template, creating a peer assessment form has never been easier. The links will provide you with a pre-populated form, complete with all the necessary sections and items, saving you time and effort in setting up the form from scratch. Whether you are a module convener or a teaching assistant, this template is a great starting point for conducting peer assessments using Microsoft Forms.


**Remarks:**

- pygla is sensitive to the Microsoft section orientation, so the above order should be followed when designing the Microsoft Form.

# Using data from Microsoft Word Form

pygla allows for input from a Microsoft Word form, offering a more user-friendly alternative to the original implementation. One of the common mistakes made in the old system was confusion over whether to enter data vertically or horizontally.

To input data from a Microsoft Word form, the user must first create an Excel file with the following headers, in the specified order and with the specified nomenclature:

- name	
- assessor\_student\_id	
- group\_name	
- peer\_name	
- peer\_student\_id	
- research\_information\_gathering	
- creative\_input	
- cooperation\_within\_group	
- communication	
- contribution\_quality	
- meeting\_attendance	
- justification

A detailed description for each of the column is as follows.

- **name**: This is the name of the contributor.
- **assessor\_student\_id**: This is the registered university student ID that is usually used to tie to the student's mark.
- **group\_name**: This is the information about the student's assigned group. Pygla only accepts group names in integer format (e.g. 1, 2, 3, etc.).
- **peer\_name**: This is the name of the fellow group member being rated.
- **peer\_student\_id**: This is the registered university student ID of the fellow group member being rated.
- research\_information\_gathering: This is the rating for the Research & Information gathering
- creative\_input: This is the rating for the Creative input
- cooperation\_within\_group: This is the rating for the Co-operation within group
- communication: This is the rating for the Communication within group
- contribution\_quality: This is the rating for the Quality of individual contributions
- meeting\_attendance: This is the rating for the Attendance at meetings
- justification: This is the justification provided by the assessor to justify their ratings for each peer assessment criterion.

For reference, user can refer to the file “**peer\_assessment\_word2excel.xlsx**” which is available in the repo

# Limitation
The limitation of pygla is that it assumes every member of the group will provide an assessment to all of their peers.

# TODO
1. What should we do if some peers have not contributed to the assessment? Should we assume that the assessor will give the highest mark by default?
1. What should we do if peer factor that greater than 1.2? Should we adjust/ normalize this value?
1. To support peer assessment conducted via the Moodle page. 
