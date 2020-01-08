import React, { Component } from "react";
import "./Analysis.css";
import Select from "react-dropdown-select";
import LineChart from "./Charts/AnalysisChart";
import Button from "react-bootstrap/Button";

class Analysis extends Component {
  state = {
    timeOption: [
      {
        label: "Last Hour",
        value: "Last Hour"
      },
      {
        label: "Last Day",
        value: "Last Day"
      },
      {
        label: "Specific",
        value: "Specific"
      }
    ],
    chartOption: [
      {
        label: "Linear Chart",
        value: "Linear Chart"
      },
      {
        label: "Tabular Form",
        value: "Tabular Form"
      }
    ]
  };
  chartClick = label => {
    const chartType = Object.create(this.state.chartOption);
    for (let key in this.state.chartOption) {
      if (key !== label) {
      }
    }
  };

  render() {
    {
      createChartType();
    }
    const { timeOption, chartOption } = this.state;
    let chart: any = [];
    if (chartOption)
      return (
        <div className="container-truex">
          <div className="topbar">
            <Button className="button" variant="dark" size="lg">
              Video Analysis
            </Button>
            <div className="selectionbar">
              <div className="dropdown">
                <label>Time Selection</label>
                <Select
                  className="timeselection"
                  options={this.state.timeOption}
                  placeholder={this.state.timeOption[0].label} // By default should be "Last Hour"
                />
              </div>
              <div className="dropdown">
                <label>Chart Type </label>
                <Select
                  className="charttype"
                  options={this.state.chartOption}
                  placeholder={this.state.chartOption[0].label} // By default should be "Linear Chart"
                  onclick={this.chartClick}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="analysis-box-part">
              <div>
                <LineChart
                  timeData={[1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]}
                  peopleCount={[0, 53, 75, 24, 70, 321, 43, 234, 26, 0]}
                />
              </div>
            </div>
          </div>
        </div>
      );
  }
}

function createChartType() {
  console.log("createChartType");
  return null;
}
export default Analysis;
