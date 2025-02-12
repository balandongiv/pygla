
LEN_COLS_MQUIZ=13




COLS_OPT = [
    [
        'std_name',
     'research_information_gathering',
     'creative_input',
     'cooperation_within_group',
     'communication',
     'contribution_quality',
     'meeting_attendance',
     'dgroup_name',
     'nmember',
     'weightage',
     'justification_annom',
     'feedback'
     ]
]

D_AGG_CALCULATION = {
    "peer_student_id_validation": "first",
    "peer_name": "first",
    "group_name": "first",
    "research_and_information_gathering": "mean",
    "creative_input": "mean",
    "co_operation_within_group": "mean",
    "communication_withing_group": "mean",
    "quality_of_individual_contribution": "mean",
    "attendance_at_meeting": "mean",
    "feedback": "\n".join,
    "justification_annom": "\n".join
}

REMAP_VALUES = {
    "Terrible (0)": "0",
    "Very Poor (1)": "1",
    "Poor (2)": "2",
    "Adequate (3)": "3",
    "Good (4)": "4",
    "Very Good (5)": "5",
    "Excellent (6)": "6"
}

COL_NAME = [
    "id", "start_time", "completion_time", "email", "name", "assessor_student_id", "group_name",
    "peer_name", "peer_student_id",
    "research_and_information_gathering", "creative_input", "co_operation_within_group",
    "communication_withing_group", "quality_of_individual_contribution", "attendance_at_meeting",
    "justification"
]

COLUMN_TO_KEEP=[
    'std_id',
                'weightage',
                'group_name',
                'std_name',
                'research_and_information_gathering',
                'creative_input',
                'co_operation_within_group',
                'communication_withing_group',
                'quality_of_individual_contribution',
                'attendance_at_meeting',
                'dgroup_name',
                'nmember',
                'weightage',
                'justification_annom',
                'feedback'
                ]


N_ELEMENT = [
    "research_and_information_gathering", "creative_input", "co_operation_within_group",
    "communication_withing_group", "quality_of_individual_contribution", "attendance_at_meeting"
]

CONST_VAL = {
    "research_and_information_gathering": 15,
    "creative_input": 20,
    "co_operation_within_group": 15,
    "communication_withing_group": 15,
    "quality_of_individual_contribution": 20,
    "attendance_at_meeting": 15
}