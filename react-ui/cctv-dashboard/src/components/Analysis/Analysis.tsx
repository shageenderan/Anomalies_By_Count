import React from "react";
import "./Analysis.css";
import Select from "react-dropdown-select";
import LineChart from "./Charts/AnalysisChart";
import Button from "react-bootstrap/Button";

interface AnalysisProps {
  match: any
  data: {
    [id: number]: {
      show: boolean, label: string, url: string, maximise: boolean,
      showCam: "hidden" | "show", showUrl: "hidden" | "show", videoId: number, peopleCount: number[], timeData: number[]
    }
  };
}

interface AnalysisState {
  timeSelection: { label: string, value: string };
  chartType: { label: string, value: string };
}

class Analysis extends React.Component<AnalysisProps, AnalysisState> {
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

  componentDidMount() {
    console.log("data from analysis:", this.props)
  }

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
    const player = this.props.data[this.props.match.params.id]
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
              {player.timeData.length ?
                <LineChart
                  timeData={player.timeData}
                  peopleCount={player.peopleCount}
                />
                :
                <h2>No data to display</h2>
              }

            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Analysis;
