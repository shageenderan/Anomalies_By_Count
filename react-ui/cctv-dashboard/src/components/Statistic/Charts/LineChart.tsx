import React from "react";
import Chart from "react-apexcharts";
import "./LineChart.css";
import Button from "react-bootstrap/Button";

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
      <div className="chart">
        <Chart
          options={options}
          series={[{ data: this.props.peopleCount }]}
          type="line"
        />
      </div>
    );
  }
}

function createChart({ timeData, peopleCount, click, show, id, text }) {
  if (!show) return null;

  return (
    <div className="col-sm-6 ">
      <a href="#" />
      <div className="box-part text-center " onClick={() => click(id)}>
        <div className="title"></div>
        <Button className="text" variant="dark" size="lg">
          {text}
        </Button>
        <div className="chart">
          <LineChart timeData={timeData} peopleCount={peopleCount} />
        </div>
      </div>
    </div>
  );
}

export default createChart;
