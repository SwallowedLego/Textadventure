const message = document.getElementById("message");
const buttons = document.querySelectorAll("button[data-choice]");

const responses = {
  "1": "Starting a new adventure...",
  "2": "No saved adventure was found yet.",
  "3": "Goodbye, adventurer!"
};

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const choice = button.dataset.choice;
    message.textContent = responses[choice] ?? "Invalid choice. Please enter 1, 2, or 3.";

    if (choice === "3") {
      buttons.forEach((item) => {
        if (item.dataset.choice !== "3") {
          item.disabled = true;
        }
      });
    }
  });
});
