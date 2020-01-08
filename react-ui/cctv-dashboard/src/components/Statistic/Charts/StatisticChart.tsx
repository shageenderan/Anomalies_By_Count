import React from "react";
import Chart from "react-apexcharts";
import "./StatisticChart.css";
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
      <Chart
        options={options}
        series={[{ data: this.props.peopleCount }]}
        type="line"
      />
    );
  }
}

function createStatChart({
  timeData,
  peopleCount,
  click,
  show,
  id,
  text,
  maximise
}) {
  if (!show) return null;

  let cName: string = maximise ? "maximise-box-part" : "statistic-box-part";
  return (
    <div className="col-md-6 ">
      <a href="#" />
      <div className={cName + " text-center"} onClick={() => click(id)}>
        <Button className="text" variant="dark" size="lg">
          {text}
        </Button>
        <LineChart timeData={timeData} peopleCount={peopleCount} />
      </div>
    </div>
  );
}

export default createStatChart;