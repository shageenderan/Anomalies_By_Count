import React, { Component } from "react";
import "./Analysis.css";
import Select from "react-dropdown-select";
import LineChart from "./Charts/AnalysisChart";
import Button from "react-bootstrap/Button";

class Analysis extends Component {  
   timeOptions = [
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
  ];
  
  chartOptions = [
    {
      label: "Linear Chart",
      value: "Linear Chart"
    },
    {
      label: "Tabular Form",
      value: "Tabular Form"
    }
  ];

  state = {
    timeSelection: this.timeOptions[0],
    chartType: this.chartOptions[0]
   };

  handleChangeTimeSelection = values => {
    this.setState({ timeSelection: values.length ? values[0] : null });
  }

  handleChangeChartType = values => {
    console.log('change chart type:');
    console.log(values);
    this.setState({ chartType: values.length ? values[0] : null });
  }

  render() {
    const { timeSelection, chartType } = this.state;
    const isSpecificTime = timeSelection === this.timeOptions[2];

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
                options={this.timeOptions}
                onChange={this.handleChangeTimeSelection}
                values={[timeSelection]}
              />
              {isSpecificTime &&
            <>
              <div>
                <label>From Time</label>
                <input type="date" />
              </div>
              <div>
                <label>To Time</label>
                <input type="date" />
              </div>
            </>
            }
            </div>
            <div className="dropdown">
              <label>Chart Type </label>
              <Select
                className="charttype"
                options={this.chartOptions}
                onChange={this.handleChangeChartType}
                values={[chartType]}
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

export default Analysis;
