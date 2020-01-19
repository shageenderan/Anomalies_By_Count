import React from "react";
import Chart from "react-apexcharts";
import "./AnalysisChart.css";

type MyState = { timeData: number[]; peopleCount: number[], valMax: number};

class LineChart extends React.Component<MyState, {}> {
  render() {
    var options = {
      chart: {
        zoom: {
          enabled: true
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
        type: 'numeric',
        categories: this.props.timeData,
        labels: {
          style: {
            fontSize: "16px"
          }
        },
        title:{
          text: 'Time (s)'
        },
        tickAmount: 10,
        min: 0,
        max: this.props.valMax,
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

function createAnalysisChart({ timeData, peopleCount, valMax }) {
  return <LineChart timeData={timeData} peopleCount={peopleCount} valMax={valMax}/>;
}
export default createAnalysisChart;
