import React from "react";
import "./Analysis.css";
import Select from "react-dropdown-select";
import LineChart from "./Charts/LineChart";
import Button from "react-bootstrap/Button";
import Dropdown from "react-dropdown";

const timeOption = [
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
const chartOption = [
  {
    label: "Linear Chart",
    value: "Linear Chart"
  },
  {
    label: "Tabular Form",
    value: "Tabular Form"
  }
];

function Analysis() {
  return (
    <div className="box">
      <div className="topbar">
        <Button className="button" variant="dark" size="lg">
          Video Analysis
        </Button>
      </div>

      <div>
        <LineChart />
      </div>

      <div className="selectionbar">
        <div className="dropdown">
          Time Selection
          <Select
            className="timeselection"
            options={timeOption}
            placeholder={timeOption[0].label} // By default should be "Last Hour"
          />
        </div>
        <div className="dropdown">
          Chart Type
          <Select
            className="charttype"
            options={chartOption}
            placeholder={chartOption[0].label} // By default should be "Linear Chart"
          />
        </div>
      </div>
    </div>
  );
}

export default Analysis;
