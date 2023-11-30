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
    const body = document.body;
    const section = document.getElementById("network-statistics")
    const table = document.createElement('table');
    const table_header = document.createElement('thead')
    const table_body = document.createElement('tbody')

    // Create header row
    const header_row = document.createElement('tr');
    headers = ["Dataset Name", "Num. nodes", "Num. edges", "Min edge size", "Max edge size", "Num. components"]
    for (const i in headers) {
        const h = document.createElement('th');
        h.textContent = headers[i];
        header_row.appendChild(h)
    }
    table_header.appendChild(header_row)

    // Create data rows
    for (const key in json_data) {
        const data_row = document.createElement('tr');

        // dataset name
        const td_name = document.createElement('td');
        td_name.innerHTML = '<a href=' + json_data[key]["url"] + '>key</a>';
        data_row.appendChild(td_name);

        // number of nodes
        const td_num_nodes = document.createElement('td');
        if (json_data[key]["num-nodes"]) {
            td_num_nodes.textContent = json_data[key]["num-nodes"];
        }
        else {
            td_num_nodes.textContent = "N/A"
        }
        data_row.appendChild(td_num_nodes);

        // number of edges
        const td_num_edges = document.createElement('td');
        if (json_data[key]["num-edges"]) {
            td_num_edges.textContent = json_data[key]["num-edges"];
        }
        else {
            td_num_edges.textContent = "N/A"
        }
        data_row.appendChild(td_num_edges);

        // min edge size
        const td_min_edge_size = document.createElement('td');
        if (json_data[key]["min-edge-size"]) {
            td_min_edge_size.textContent = json_data[key]["min-edge-size"];
        }
        else {
            td_min_edge_size.textContent = "N/A"
        }
        data_row.appendChild(td_min_edge_size);

        // max edge size
        const td_max_edge_size = document.createElement('td');
        if (json_data[key]["max-edge-size"]) {
            td_max_edge_size.textContent = json_data[key]["max-edge-size"];
        }
        else {
            td_max_edge_size.textContent = "N/A"
        }
        data_row.appendChild(td_max_edge_size);

        // number of components
        const td_num_components = document.createElement('td');
        if (json_data[key]["num-components"]) {
            td_num_components.textContent = json_data[key]["num-components"];
        }
        else {
            td_num_components.textContent = "N/A"
        }
        data_row.appendChild(td_num_components);
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