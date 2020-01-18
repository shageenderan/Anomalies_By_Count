import React from "react";
import Chart from "react-apexcharts";
import "./StatisticChart.css";
import Button from "react-bootstrap/Button";

type MyProps = { timeData: number[]; peopleCount: number[], valMax:number };

class LineChart extends React.Component<MyProps, {}> {
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
        seriesName: 'People Count',
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
  maximise,
  valMax }){
  if (!show) return null;

  let cName: string = maximise ? "maximise-box-part" : "statistic-box-part";
  return (
    <div className="col-md-6 ">
      <a href="#" />
      <div className={cName + " text-center"}>
        <Button className="text" variant="dark" size="lg" onClick={() => click(id)}>
          {text}
        </Button>
        <LineChart timeData={timeData} peopleCount={peopleCount} valMax={valMax}/>
      </div>
    </div>
  );
}

export default createStatChart;
