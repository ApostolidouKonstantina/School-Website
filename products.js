const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const getSearchButton = document.getElementById("getSearch");
    getSearchButton.onclick = searchButtonOnClick;
    const postReqButton = document.getElementById("postReq");
    postReqButton.onclick = productFormOnSubmit;
    // END CODE HERE
  }

  searchButtonOnClick = () => {
    const getName = document.getElementById("getName")
    // BEGIN CODE HERE
    const res = new XMLHttpRequest();
    res.open("GET", `${api}/search?name=${getName.value}`);
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {
                const resText = JSON.parse(res.responseText);
              
                let col = [];
                col.push("_id");
                col.push("name");
                col.push("production_year");
                col.push("price");
                col.push("color");
                col.push("size");

                // Create a table.
                const table = document.createElement("table");
                table.style="width: 1200px" ;

                // Create table header row using the extracted headers above.
                let tr = table.insertRow(-1);   

                // add json data to the table as rows.
                for (let i = 0; i < resText.length; i++) {

                    tr = table.insertRow(-1);

                    for (let j = 0; j < col.length; j++) {
                        let tabCell = tr.insertCell(-1);
                        tabCell.style="width: 200px";
                        tabCell.innerHTML = resText[i][col[j]];
                }
                }

                // Now, add the newly created table with json data, to a container.
                const divShowData = document.getElementById('resultsTable');
                divShowData.innerHTML = "";
                divShowData.appendChild(table);
                        
                        }
                    }
                };
    res.send();
    // END CODE HERE
}



productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    const name = document.getElementById("name");
    const production_year = document.getElementById("productionyear");
    const price = document.getElementById("price");
    const color = document.getElementById("color");
    const size = document.getElementById("size");
    const res = new XMLHttpRequest();
    res.open("POST", `${api}/add-product?name=${name.value}&production_year=${production_year.value}&price=${price.value}&color=${color.value}&size=${size.value}`);
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {
                alert("OK");
            }
        }
    };
    res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    //erase form
    const inputs = document.querySelectorAll('#name, #productionyear, #price, #price, #color, #size');
    inputs.forEach(input => { input.value = ''; });
    res.send();
    // END CODE HERE
}
