import { useState, useEffect } from "react";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import LineChart from './LineChart';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function App() {
    const [file, setFile] = useState(null);
    const [summary, setSummary] = useState(null);
    const [datasets, setDatasets] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState(null);
    const [statsByType, setStatsByType] = useState([]);

    useEffect(() => {
        fetchDatasets();
        fetchStatsByType();
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

    const fetchStatsByType = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/stats/");
            const data = await response.json();
            setStatsByType(data);
        } catch (error) {
            console.error("Error fetching stats:", error);
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
            fetchStatsByType();
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

    // Student 4 - Delete dataset
    const deleteDataset = async (datasetId) => {
        if (!window.confirm("Are you sure you want to delete this dataset?")) return;
        try {
            await fetch(`http://127.0.0.1:8000/api/datasets/${datasetId}/delete/`, { method: 'DELETE' });
            fetchDatasets();
            fetchStatsByType();
            setSummary(null);
            alert("Dataset deleted successfully!");
        } catch (error) {
            console.error("Error deleting dataset:", error);
        }
    };

    // Student 1 - Search equipment
    const searchEquipment = async () => {
        if (!searchQuery.trim()) return;
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/search/?q=${searchQuery}`);
            const data = await response.json();
            setSearchResults(data);
        } catch (error) {
            console.error("Error searching:", error);
        }
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
                <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
                <button onClick={uploadFile}>Upload CSV</button>
            </div>

            {/* Student 1 - Search */}
            <div className="search-section">
                <h2>Search Equipment</h2>
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search by name or type (e.g. pump)"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && searchEquipment()}
                    />
                    <button onClick={searchEquipment}>Search</button>
                    {searchResults && <button onClick={() => setSearchResults(null)}>Clear</button>}
                </div>
                {searchResults && (
                    <div className="search-results">
                        <p>{searchResults.count} result(s) found</p>
                        {searchResults.count > 0 && (
                            <table>
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Type</th>
                                        <th>Flowrate</th>
                                        <th>Pressure</th>
                                        <th>Temperature</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {searchResults.results.map((eq, i) => (
                                        <tr key={i}>
                                            <td>{eq.equipment_name}</td>
                                            <td>{eq.equipment_type}</td>
                                            <td>{eq.flowrate}</td>
                                            <td>{eq.pressure}</td>
                                            <td>{eq.temperature}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}
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
                                {/* Student 4 - Delete */}
                                <button className="delete-btn" onClick={() => deleteDataset(dataset.id)}>Delete</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Student 2 - Stats by Type */}
            {statsByType.length > 0 && (
                <div className="stats-by-type-section">
                    <h2>Stats by Equipment Type</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Avg Flowrate</th>
                                <th>Min Flowrate</th>
                                <th>Max Flowrate</th>
                                <th>Avg Pressure</th>
                                <th>Avg Temperature</th>
                            </tr>
                        </thead>
                        <tbody>
                            {statsByType.map((s, i) => (
                                <tr key={i}>
                                    <td>{s.equipment_type}</td>
                                    <td>{s.avg_flowrate?.toFixed(2)}</td>
                                    <td>{s.min_flowrate?.toFixed(2)}</td>
                                    <td>{s.max_flowrate?.toFixed(2)}</td>
                                    <td>{s.avg_pressure?.toFixed(2)}</td>
                                    <td>{s.avg_temperature?.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

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

                    {/* Student 3 - Line Chart */}
                    {summary.equipment && (
                        <div className="chart-container">
                            <LineChart equipment={summary.equipment} />
                        </div>
                    )}

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
