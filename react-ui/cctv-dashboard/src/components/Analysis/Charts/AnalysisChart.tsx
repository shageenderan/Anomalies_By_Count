import React from "react";
import Chart from "react-apexcharts";
import "./AnalysisChart.css";

type MyState = { timeData: number[]; peopleCount: number[] };

class LineChart extends React.Component<MyState, {}> {
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
        categories: this.props.timeData,
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
      <Chart
        options={options}
        series={[{ data: this.props.peopleCount }]}
        type="line"
      />
    );
  }
}

function createAnalysisChart({ timeData, peopleCount }) {
  return <LineChart timeData={timeData} peopleCount={peopleCount} />;
}
export default createAnalysisChart;
