import React from "react";
import Chart from "react-apexcharts";
import "./LineChart.css";

class LineChart extends React.Component {
  render() {
    var options = {
      chart: {
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: true
      },
      stroke: {
        curve: "straight"
      },
      title: {
        text: "People Count",
        align: "left",
        style: {
          fontSize: "25px",
          fontFamily: "bold"
        }
      },
      xaxis: {
        categories: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        labels: {
          style: {
            fontSize: "16px"
          }
        }
      },
      yaxis: {
        labels: {
          style: { fontSize: "16px" }
        }
      }
    };

    return (
      <div className="chart">
        <Chart
          options={options}
          series={[{ data: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0] }]}
          type="line"
          width="70%"
        />
      </div>
    );
  }
}

export default LineChart;
