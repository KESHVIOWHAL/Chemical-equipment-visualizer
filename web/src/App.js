import { useState, useEffect } from "react";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function App() {
    const [file, setFile] = useState(null);
    const [summary, setSummary] = useState(null);
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState(null);

    useEffect(() => {
        fetchDatasets();
    }, []);

    const fetchDatasets = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/datasets/");
            const data = await response.json();
            setDatasets(data);
        } catch (error) {
            console.error("Error fetching datasets:", error);
        }
    };

    const uploadFile = async () => {
        if (!file) {
            alert("Please select a CSV file");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/upload/", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            setSummary(data);
            fetchDatasets();
            alert("File uploaded successfully!");
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Upload failed");
        }
    };

    const viewDataset = async (datasetId) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/datasets/${datasetId}/`);
            const data = await response.json();
            setSelectedDataset(data);
            setSummary({
                total_count: data.total_count,
                avg_flowrate: data.avg_flowrate,
                avg_pressure: data.avg_pressure,
                avg_temperature: data.avg_temperature,
                type_distribution: data.type_distribution,
                equipment: data.equipment
            });
        } catch (error) {
            console.error("Error fetching dataset:", error);
        }
    };

    const downloadPDF = (datasetId) => {
        window.open(`http://127.0.0.1:8000/api/datasets/${datasetId}/pdf/`, '_blank');
    };

    const barChartData = summary ? {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [{
            label: 'Average Values',
            data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
            backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(255, 206, 86, 0.6)'],
            borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(255, 206, 86, 1)'],
            borderWidth: 1
        }]
    } : null;

    const pieChartData = summary && summary.type_distribution ? {
        labels: Object.keys(summary.type_distribution),
        datasets: [{
            data: Object.values(summary.type_distribution),
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
            ],
            borderWidth: 1
        }]
    } : null;

    return (
        <div className="container">
            <h1>Chemical Equipment Parameter Visualizer</h1>
            
            <div className="upload-section">
                <h2>Upload CSV File</h2>
                <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files[0])}
                />
                <button onClick={uploadFile}>Upload CSV</button>
            </div>

            <div className="history-section">
                <h2>Dataset History (Last 5)</h2>
                <div className="dataset-list">
                    {datasets.map((dataset) => (
                        <div key={dataset.id} className="dataset-item">
                            <span>{dataset.name} - {new Date(dataset.uploaded_at).toLocaleString()}</span>
                            <div>
                                <button onClick={() => viewDataset(dataset.id)}>View</button>
                                <button onClick={() => downloadPDF(dataset.id)}>Download PDF</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {summary && (
                <div className="results-section">
                    <h2>Summary Statistics</h2>
                    <div className="stats-grid">
                        <div className="stat-card">
                            <h3>Total Equipment</h3>
                            <p>{summary.total_count}</p>
                        </div>
                        <div className="stat-card">
                            <h3>Avg Flowrate</h3>
                            <p>{summary.avg_flowrate?.toFixed(2) || '0.00'}</p>
                        </div>
                        <div className="stat-card">
                            <h3>Avg Pressure</h3>
                            <p>{summary.avg_pressure?.toFixed(2) || '0.00'}</p>
                        </div>
                        <div className="stat-card">
                            <h3>Avg Temperature</h3>
                            <p>{summary.avg_temperature?.toFixed(2) || '0.00'}</p>
                        </div>
                    </div>

                    <div className="charts-section">
                        <div className="chart-container">
                            <h3>Average Parameters</h3>
                            {barChartData && <Bar data={barChartData} />}
                        </div>
                        <div className="chart-container">
                            <h3>Equipment Type Distribution</h3>
                            {pieChartData && <Pie data={pieChartData} />}
                        </div>
                    </div>

                    {summary.equipment && (
                        <div className="table-section">
                            <h3>Equipment Details</h3>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Equipment Name</th>
                                        <th>Type</th>
                                        <th>Flowrate</th>
                                        <th>Pressure</th>
                                        <th>Temperature</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {summary.equipment.map((eq, index) => (
                                        <tr key={index}>
                                            <td>{eq.equipment_name || eq['Equipment Name']}</td>
                                            <td>{eq.equipment_type || eq['Type']}</td>
                                            <td>{eq.flowrate || eq['Flowrate']}</td>
                                            <td>{eq.pressure || eq['Pressure']}</td>
                                            <td>{eq.temperature || eq['Temperature']}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default App;
