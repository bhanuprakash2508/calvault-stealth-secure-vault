/* Secret Date Selection */

let selectedDates = [];

function toggleDate(element) {

    const day = element.dataset.day;

    if (
        element.classList.contains("selected")
    ) 
    {

        element.classList.remove(
            "selected"
        );

        selectedDates = selectedDates.filter(
            d => d !== day
        );
    }

    else {

        if (selectedDates.length >= 4) {

            alert(
                "Only 4 dates allowed"
            );

            return;
        }

        element.classList.add(
            "selected"
        );

        selectedDates.push(day);
    }

    updateSelection();
}

/* Update UI */

function updateSelection() {

    const text = document.getElementById(
        "selectedText"
    );

    const input = document.getElementById(
        "calendarPattern"
    );

    if (selectedDates.length > 0) {

        text.innerText =
            "Selected: " +
            selectedDates.join(" - ");
    }

    else {
        text.innerText =
            "Selected: None";
    }

    input.value = selectedDates.join(",");
}