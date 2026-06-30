/* Global Variables */

let clickedDates = [];
let calendar = null;
let allEvents = [];
let editingEventId = null;
let secretUnlocked = false;

/* Initial Load */

document.addEventListener("DOMContentLoaded", function () {
    initializeCalendar();
    initializeCreateButton();
    initializeSearch();
});

/* Calendar Initialization */

function initializeCalendar() {

    const calendarEl = document.getElementById("calendar");

    allEvents = existingEvents;

    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        height: "90vh",
        events: allEvents,

        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: ""
        },

        dateClick: function (info) {

            let day = new Date(
                info.dateStr
            ).getDate();

            trackSecretPattern(day);
        },

        eventClick: function (info) {
            openEditModal(
                info.event
            );
        }
    });

    calendar.render();

    document.addEventListener(
        "dblclick",
        function (e) {

            if (
                e.target.classList.contains(
                    "fc-toolbar-title"
                )
            ) {
                triggerVault();
            }
        }
    );
}

/* Create Button */

function initializeCreateButton() {

    const btn = document.querySelector(".create-btn");

    if (!btn) return;

    btn.addEventListener("click", function () {
        openModal();
    });
}

/* Modal Functions */

function openModal() {

    editingEventId = null;

    document.getElementById("modalTitle").innerText = "Add Item";
    document.getElementById("eventTitle").value = "";
    document.getElementById("eventDate").value = "";
    document.getElementById("eventDescription").value = "";

    document.getElementById("saveBtn").style.display = "block";
    document.getElementById("updateBtn").style.display = "none";
    document.getElementById("deleteBtn").style.display = "none";

    document.getElementById("eventModal").style.display = "flex";
}


function closeModal() {
    document.getElementById("eventModal").style.display = "none";
}

/* Save Event */

function saveEvent() {

    fetch("/add-event", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: document.getElementById("eventTitle").value,
            type: document.getElementById("eventType").value,
            date: document.getElementById("eventDate").value,
            description: document.getElementById("eventDescription").value
        })
    })

    .then(response => response.json())

    .then(data => {
        if (data.status === "success") {
            location.reload();
        }
    });
}

/* Open Edit Modal */

function openEditModal(event) {

    editingEventId = event.id;

    document.getElementById("modalTitle").innerText = "Edit Item";
    document.getElementById("eventTitle").value = event.title;
    document.getElementById("eventType").value = event.extendedProps.type;
    document.getElementById("eventDate").value = event.startStr;
    document.getElementById("eventDescription").value =
        event.extendedProps.description;

    document.getElementById("saveBtn").style.display = "none";
    document.getElementById("updateBtn").style.display = "block";
    document.getElementById("deleteBtn").style.display = "block";

    document.getElementById("eventModal").style.display = "flex";
}

/* Update Event */

function updateEvent() {

    fetch(`/update-event/${editingEventId}`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: document.getElementById("eventTitle").value,
            type: document.getElementById("eventType").value,
            date: document.getElementById("eventDate").value,
            description: document.getElementById("eventDescription").value
        })
    })

    .then(response => response.json())

    .then(data => {
        if (data.status === "success") {
            location.reload();
        }
    });
}

/* Delete Event */

function deleteEvent() {

    fetch(`/delete-event/${editingEventId}`, {
        method: "POST"
    })

    .then(response => response.json())

    .then(data => {
        if (data.status === "success") {
            location.reload();
        }
    });
}

/* Filter Events */

function filterEvents(type) {

    if (!calendar) return;

    calendar.removeAllEvents();

    let filtered = [];

    if (type === "all") {
        filtered = allEvents;
    }

    else {
        filtered = allEvents.filter(
            event => event.type === type
        );
    }

    filtered.forEach(function (event) {
        calendar.addEvent(event);
    });
}

/* Secret Pattern Tracker */

function trackSecretPattern(day) {

    clickedDates.push(day);

    if (clickedDates.length > 4) {
        clickedDates.shift();
    }

    verifyPattern();
}

/* Verify Secret Pattern */

function verifyPattern() {

    fetch("/verify-pattern", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            sequence: clickedDates
        })
    })

    .then(response => response.json())

    .then(data => {

        if (data.status === "success") {
            secretUnlocked = true;

            console.log(
                "Secret pattern accepted"
            );
        }
    });
}

/* Vault Trigger */

function triggerVault() {

    console.log(
        "Double click detected"
    );

    if (secretUnlocked) {
        window.location.href = "/vault-auth";
    }

    else {
        console.log(
            "Secret pattern not entered"
        );
    }
}

/* Search Events */

function initializeSearch() {

    const searchBox = document.getElementById(
        "searchEvents"
    );

    if (!searchBox) return;

    searchBox.addEventListener(
        "input",
        function () {

            const query = this.value
                .toLowerCase()
                .trim();

            calendar.removeAllEvents();

            const filtered = allEvents.filter(
                event =>
                    event.title
                        .toLowerCase()
                        .includes(query)
            );

            filtered.forEach(function (event) {
                calendar.addEvent(event);
            });
        }
    );
}

let recoveryTap = 0;

/* PREVENT TEXT SELECTION */

document.getElementById(
    "plannerTitle"
).addEventListener(
    "mousedown",
    function(e){
        e.preventDefault();
    }
);

/* RECOVERY ACCESS */

document.getElementById(
    "plannerTitle"
).addEventListener(
    "click",
    function(){

        recoveryTap++;

        if(recoveryTap === 5){

            window.location.href =
                "/recover-access";
        }

        setTimeout(
            function(){
                recoveryTap = 0;
            },
            3000
        );
    }
);