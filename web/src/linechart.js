import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function LineChart({ equipment }) {
    if (!equipment || equipment.length === 0) return null;

    const labels = equipment.map((eq) => eq.equipment_name || eq['Equipment Name']);

    const data = {
        labels,
        datasets: [
            {
                label: 'Flowrate',
                data: equipment.map((eq) => eq.flowrate || eq['Flowrate']),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
            },
            {
                label: 'Pressure',
                data: equipment.map((eq) => eq.pressure || eq['Pressure']),
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.4,
            },
            {
                label: 'Temperature',
                data: equipment.map((eq) => eq.temperature || eq['Temperature']),
                borderColor: 'rgba(255, 206, 86, 1)',
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                tension: 0.4,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Equipment Parameter Trends' },
        },
    };

    return (
        <div style={{ marginTop: '2rem' }}>
            <h3>Parameter Trends</h3>
            <Line data={data} options={options} />
        </div>
    );
}

export default LineChart;