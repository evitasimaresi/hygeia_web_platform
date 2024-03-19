////////////////////////////
// Ajax Register and Login//
////////////////////////////
function auth_user(action) {
    // create new ajax object
    var ajax = new XMLHttpRequest();

    // when page is loaded, have a callback function pre-fill our div
    ajax.onreadystatechange = function () {
        if (ajax.readyState == 4 && ajax.status == 200) {
            // $('#infodiv').html(ajax.responseText);
            document.getElementById('infodiv').innerHTML = ajax.responseText;
        }
    };
    console.log(action)
    // open request file and transmit data
    ajax.open('GET', action, true);
    ajax.send();

}

////////////////////////////////////////////
// Load register when page initially loads//
////////////////////////////////////////////
window.onload = function () {
    // auth_user("register"); //When it run whenever i load a window the function is called, which i dont want this
};


// Show specialty field on register only when doctor is selected
function toggleSpecialtyfield() {
    var doctorselected = document.querySelector('input[name="user_type"][value="doctor"]');
    var specialtyfield = document.getElementById('specialtyfield');
    if (doctorselected && doctorselected.checked) {
        specialtyfield.style.display = doctorselected = 'block';
    } else {
        specialtyfield.style.display = 'none';
    }
}

// document.addEventListener('DOMContentLoaded', toggleSpecialtyfield);

/////////////
// Load DOM//
/////////////
// document.addEventListener('DOMContentLoaded', function() {
//   // Log to confirm
//   console.log("Script loaded and DOM fully loaded.");

//   var input = document.getElementById("symptoms");


//   // Attach the keypress event listener to the input element
//   input.addEventListener("keypress", function(event) {
//       if (event.key === "Enter") {
//           event.preventDefault();
//       console.log("Symptoms are:", input.value);
//     }
// })
// });

function removeevent() {
    input.removeEventListener("keypress", handleKeypress);
}

/////////////////////////////////////////////////////////////
// Show available doctors for choosen specialty on chat tab//
/////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {
    const specialtySelects = document.querySelectorAll('select[name="specialty"]');
    if (specialtySelects) {
        specialtySelects.forEach(function (specialtySelect) {
            specialtySelect.addEventListener('change', function () {
                const selectedSpecialty = this.value;
                const doctorSelect = document.getElementById('doctor_' + this.id.split('_')[1]);
                getdoctors(selectedSpecialty, doctorSelect);
            });
        });
    } else {
        console.error('Element with id "choosespecialty" not found.')
    }
});

// Ajax
function getdoctors(specialty_id, doctorSelect) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var doctors = JSON.parse(this.responseText);
            updateDoctorlist(doctors, doctorSelect);
            // document.getElementById("placedoctors").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_doctor_by_specialty?specialty_id=" + encodeURIComponent(specialty_id), true);
    xhttp.send();
}

function updateDoctorlist(doctors, doctorSelect) {
    // var doctorListelemnt = document.getElementById('doctorSelection');
    // doctorListelemnt.innerHTML = '';

    doctorSelect.innerHTML = '<option selected="" disabled="" value="">Choose doctor</option>';

    doctors.forEach(function (doctor) {
        var option = document.createElement('option');
        option.value = doctor.id;
        option.textContent = doctor.username;
        doctorSelect.appendChild(option);
    });
}

function appointment_end(event) {
    if (!event.datetime || isNaN(Date.parse(event.datetime))) {
        console.error('Invalid start time:', event.datetime);
        console.log(event.datetime);
        return null;
    }
    var endTime = new Date(event.datetime);
    endTime.setHours(endTime.getHours() + 1);
    return endTime.toISOString();
}

// Show booking button and selected doctor after specialty
document.addEventListener('DOMContentLoaded', function () {
    const doctorSelects = document.querySelectorAll('select[name="doctor"]');
    doctorSelects.forEach(function (doctorSelect) {
        doctorSelect.addEventListener('change', function () {
            const selectedDoctor = this.value;
            const Doctorname = this.textContent.split('Choose doctor')[1];
            if (selectedDoctor) {
                const bookButtonContainer = document.getElementById('bookButton_' + this.id.split('_')[1]);
                const bookButton = document.createElement('button');
                bookButton.className = 'btn btn-primary';
                bookButton.type = 'button';
                bookButton.textContent = 'Book Appointment';
                bookButton.onclick = function () {
                    document.getElementById('doctorSelected').textContent = 'Doctor selected: ' + Doctorname
                    const trElementId = this.closest('tr').id;
                    if (trElementId) {
                        const caseId = trElementId.split('_')[1];
                        assosiateCasewithDoctor(caseId, selectedDoctor);
                    } else {
                        console.error('No <tr> element found as an ancestor of the button');
                    }
                    let calendar = initializeCalendar(CalendarConfig('book'));
                    fetsandDisplayApointments(selectedDoctor, calendar);
                };
                bookButtonContainer.innerHTML = '';
                bookButtonContainer.appendChild(bookButton);

            } else {
                const bookButtonContainer = document.getElementById('bookButtonContainer-' + this.id.split('-')[1]);
                bookButtonContainer.innerHTML = '';
            }
        });
    });
});

function assosiateCasewithDoctor(caseId, doctorId) {
    fetch('/appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'associate',
            case_id: caseId,
            doctor_id: doctorId
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


// /////////////
// // Calendar//
// /////////////

function initializeCalendar(config) {
    let calendarElement = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarElement, config);
    calendar.render();
    return calendar;
}

function CalendarConfig(action) {
    let option;
    // Default configuration
    let config = {
        themeSystem: 'bootstrap5',
        contentHeight: "auto",
        height: 10,
        aspectRatio: 2,
        allDaySlot: false,
        nowIndicator: true,
        selectable: false,
        dayRender: function (info) {
            info.el.href = null;
        }
    };

    if (action == 'book') {
        option = bookConfig();
    } else if (action == 'upcomings') {
        option = upcomingsConfig();
    }
    if (option) {
        Object.assign(config, option);
    }

    return config;
}

function bookConfig() {
    option = {
        initialView: 'timeGridWeek',
        headerToolbar: {
            // left: 'dayGridMonth,timeGridWeek,today',
            left: 'title',
            center: '',
            right: 'today,prev,next'
        },
        hiddenDays: [0, 6],
        slotMinTime: '09:00:00',
        slotMaxTime: '17:00:00',
        slotDuration: '01:00',
        selectOverlap: false,
        selectable: true,
        displayEventEnd: false,
        // eventDisplay: 'background',
        // eventRendering: 'background',
        eventColor: '#ff9f89',
        selectAllow: function (selectInfo) {
            return selectInfo.start >= new Date();
        },
        select: function (info) {
            selectEvent(calendar, info);
        },
    }
    return option;
}

function upcomingsConfig() {
    option = {
        initialView: 'listMonth',
        headerToolbar: {
            left: 'title',
            center: '',
            right: 'today,prev,next'
        },
        // eventClick: function (info) {
        //     document.getElementById('moreInfo').innerHTML = ('<h4>case information</h4> <b>Patient</b>: ' + info.event.extendedProps.moreInfo.patient_name +
        //         '<br> <b>Assigned doctor:</b> ' + info.event.extendedProps.moreInfo.doctor_name +
        //         '<br> <b>Description:</b> ' + info.event.extendedProps.moreInfo.case.description +
        //         '<br> <b>Feelings:</b> ' + info.event.extendedProps.moreInfo.case.feelings +
        //         '<br> <b>Location:</b> ' + info.event.extendedProps.moreInfo.case.location +
        //         '<br> <b>Severity:</b> ' + info.event.extendedProps.moreInfo.case.severity
        //     );
        // },
        eventClick: function (info) {
            document.getElementById('moreInfo').innerHTML = `
                <table class="appoint-details">
                    <tr>
                        <td><b>patient</b></td>
                        <td>${info.event.extendedProps.moreInfo.patient_name}</td>
                    </tr>
                    <tr>
                        <td><b>assigned doctor</b></td>
                        <td>${info.event.extendedProps.moreInfo.doctor_name}</td>
                    </tr>
                    <tr>
                        <td><b>description</b></td>
                        <td>${info.event.extendedProps.moreInfo.case.description}</td>
                    </tr>
                    <tr>
                        <td><b>feelings</b></td>
                        <td>${info.event.extendedProps.moreInfo.case.feelings}</td>
                    </tr>
                    <tr>
                        <td><b>location</b></td>
                        <td>${info.event.extendedProps.moreInfo.case.location}</td>
                    </tr>
                    <tr>
                        <td><b>severity</b></td>
                        <td>${info.event.extendedProps.moreInfo.case.severity}</td>
                    </tr>
                </table>
            `;
        }
    }
    return option;
}

    function fetsandDisplayApointments(userId, calendar) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let appointments = JSON.parse(this.responseText);
                appointments.forEach(function (appointment) {
                    calendar.addEvent({
                        title: "Booked",
                        start: appointment.datetime,
                        end: appointment_end(appointment),
                    });
                });

            }
        };
        xhttp.open("GET", "/get_appointments_by_doctor?doctor_id=" + encodeURIComponent(userId), true);
        xhttp.send();
    }

    function fetchandDisplayUpcomingAppointments(userType) {
        // Upcoming appointments
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let appointments = JSON.parse(this.responseText);
                appointments.forEach(function (appointment) {
                    let username = "";
                    if (userType == "Patient") {
                        username = appointment.doctor_name;
                    } else {
                        username = appointment.patient_name;
                    }
                    calendar.addEvent({
                        start: appointment.datetime,
                        title: "Appointment with " + username + " for " + appointment.case.description + ".",
                        moreInfo: appointment
                    });
                });

            }
        };
        xhttp.open("GET", "/get_booked_appointments", true);
        xhttp.send();
    }

    function selectEvent(calendar, info) {
        if (!info || !info.startStr) {
            console.error('No selection information provided.');
            return;
        }
        let startTime = new Date(info.startStr);
        let startTimeStr = startTime.getHours() + (startTime.getHours() >= 12 ? 'pm' : 'am');
        if (confirm('Book appointment for ' + startTimeStr + '?')) {
            fetchBookAppointment(info.startStr);
            // let endTime = appointment_end({ datetime: info.startStr });
            // let newEvent = {
            //     title: 'New Appointment',
            //     start: startTime,
            // };
            alert('Appointment confirmed for: ' + startTimeStr);
        }

        calendar.unselect();
    }

    function fetchBookAppointment(startTime) {
        fetch('/appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'book',
                start_time: startTime
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                window.location.href = '/appointments';
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    /////////////////////
    ////Index Calendar//
    ///////////////////
    // Initialize calendar for 
    document.addEventListener('DOMContentLoaded', function () {
        if (window.location.pathname === '/' || window.location.pathname === '/index') {
            let calendar = initializeCalendar(CalendarConfig('upcomings'));
            fetchandDisplayUpcomingAppointments(userType);
        }
    });

    /////////////////////////
    ////History more Info///
    ///////////////////////
    function showCaseInfo(button) {
        var caseId = button.closest('tr').id.split('_')[1];
        url = '/get_info_handled_cases?case_id=' + caseId
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network repsonse was not ok');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById(`datitme_info_${caseId}`).textContent = data.datetime;
                document.getElementById(`doctor_info_${caseId}`).textContent = `${data.doctor.username}, ${data.doctor.specialty}`;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

