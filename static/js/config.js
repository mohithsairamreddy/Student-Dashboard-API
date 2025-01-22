const dashboardConfig = {
    sections: [
        {
            id: 'personal',
            title: 'Personal Information',
            fields: [
                { id: 'name', label: 'Name', key: 'Name' },
                { id: 'username', label: 'Username', key: 'Username' },
                { id: 'gender', label: 'Gender', key: 'Gender' },
                { id: 'dob', label: 'Date of Birth', key: 'DOB', format: 'date' }
            ]
        },
        {
            id: 'academic',
            title: 'Academic Information',
            fields: [
                { id: 'class', label: 'Class', key: 'Class' },
                { id: 'section', label: 'Section', key: 'Section' },
                { id: 'medium', label: 'Medium', key: 'Medium' },
                { id: 'yearOfEnrolment', label: 'Year of Enrolment', key: 'YearOfEnrolment' }
            ]
        },
        {
            id: 'school',
            title: 'School Information',
            fields: [
                { id: 'schoolName', label: 'School Name', key: 'School_Name' },
                { id: 'schoolCode', label: 'School Code', key: 'SchoolCode' },
                { id: 'City', label: 'City', key: 'City' },
                { id: 'State', label: 'State', key: 'State' }
            ]
        }
    ]
}; 