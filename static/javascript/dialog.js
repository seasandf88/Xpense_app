const dialog = document.querySelector("dialog");
const openDialog = document.querySelector("#open-dialog");
const cancelDialog = document.querySelector("#cancel")

openDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.showModal()
});
cancelDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.close()
});
