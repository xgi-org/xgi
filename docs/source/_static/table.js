async function fetch_JSON_file(url) {
    try {
    const response = await fetch(url);

    if (!response.ok) {
       throw new Error(response);
    }

    const json_data = await response.json();
    return json_data;
    } catch (error) {
    console.error('Error fetching JSON:', error);
    }
 }

function create_table(json_data) {
    const section = document.getElementById("network-statistics")
    const table = document.createElement('table');
    table.setAttribute( "class", "data" );
    const table_header = document.createElement('thead')
    const table_body = document.createElement('tbody')

    // Create header row
    const header_row = document.createElement('tr');
    const headers = ["Dataset", "|V|", "|E|", "|E<sup>*</sup>|", "s<sub>max</sub>"]
    const header_attrs = ["num-nodes", "num-edges", "num-unique-edges", "max-edge-size"]

    for (const i in headers) {
        const h = document.createElement('th');
        h.innerHTML = headers[i];
        header_row.appendChild(h)
    }
    table_header.appendChild(header_row)

    // Create data rows
    for (const key in json_data) {
        const data_row = document.createElement('tr');

        // dataset name
        const td_name = document.createElement('td');
        const url = json_data[key]["url"].split("/files")[0]
        td_name.innerHTML = '<a href=' + url + '>' + key + '</a>';
        data_row.appendChild(td_name);

        for (const i in header_attrs){
            const td = document.createElement('td');
            const attr = header_attrs[i]
            if (json_data[key][attr]) {
                td.textContent = json_data[key][attr].toLocaleString();
            }
            else {
                td.textContent = "N/A"
            }
            data_row.appendChild(td);
        }
        table_body.appendChild(data_row);
    }
    table.appendChild(table_header)
    table.appendChild(table_body)
    console.log(table)
    section.appendChild(table);
 }

 function display_table(){
    url = 'https://raw.githubusercontent.com/xgi-org/xgi-data/main/index.json';
    data = fetch_JSON_file(url)
    .then(data => {
       // Handle the JSON data
       create_table(data);
    })
    .catch(error => {
       // Handle errors
       console.error('Error:', error);
    });
 }
