const fromLocation = document.getElementById("from_location"); // from location input
const toLocation = document.getElementById("to_location"); // to location input
const showError = document.getElementById("show_error"); // error div container
const errorSpan = showError.children[0]; // span element where we write the errors

showError.style.display = "none"; // at start

const validateForm = () => {
  if ((fromLocation.value === "import") & (toLocation.value === "export")) {
    showError.style.display = "block";
    errorSpan.innerText =
      "Can't able to import and export at same time. First try to import product to a location";

    return false;
  } else if (fromLocation.value === toLocation.value) {
    showError.style.display = "block";
    errorSpan.innerText =
      "From and to locations were same! Please change one of the location";

    return false;
  }

  showError.style.display = "none";
  return true;
};
