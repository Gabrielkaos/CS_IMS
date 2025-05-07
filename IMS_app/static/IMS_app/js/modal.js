

document.addEventListener("DOMContentLoaded", function() {
    const wrapper = document.getElementById("wrapper");
    const modal = document.getElementById("attendanceModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = document.getElementById("closeModalBtn");

    // Open the modal
    openModalBtn.addEventListener("click", function() {
      wrapper.style.display = "flex";
      modal.style.display = "flex";
      document.body.classList.add("no-scroll");
    });

    closeModalBtn.addEventListener("click", function() {
      wrapper.style.display = "none";
      modal.style.display = "none";
      document.body.classList.remove("no-scroll");
    });

    window.addEventListener("click", function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        document.body.classList.remove("no-scroll");
      }
    });
    
  });

