import React from "react";
import "./Analysis.css";
import Select from "react-dropdown-select";
import LineChart from "./Charts/AnalysisChart";
import Button from "react-bootstrap/Button";
import Table from "./Table/Table";
import axios from "axios";

// Get API URL from environment variable file
axios.defaults.baseURL = process.env.REACT_APP_API_URL

interface AnalysisProps {
  match: any
  data: {
    [id: number]: {
      show: boolean, label: string, url: string, maximise: boolean,
      showCam: "hidden" | "show", showUrl: "hidden" | "show", videoId: number, peopleCount: number[], timeData: number[]
    }
  };
}

interface Frame {
    frame_number:number;
    count:number;
    timestamp:number;
    anomaly:string;
}

interface AnalysisState {
  timeSelection: { label: string, value: string };
  chartType: { label: string, value: string };
  tableData: {[id: number]: Frame[]};
}

class Analysis extends React.Component<AnalysisProps, AnalysisState> {
  interval
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
    chartType: this.chartOptions[0],
    tableData: {
        1: [],
        2: [],
        3: [],
        4: []
        }
  };

  // Function to refresh the data shown in the table. Needs to be manual because refreshing table data will reset the
  // viewing state causing potential issues for users
  refreshTableData = (id) => {
    const players = this.props.data
    let videoId = players[id].videoId
    if (videoId !== -1) {
      let tableData = this.state.tableData;
      let url = "video/"+videoId.toString()+"/frame"
      let that = this
      axios.get(url)
           .then(res => {
              tableData[id]= res.data
              that.setState({ tableData })
           });
    }
  }


  // Function to change component shown depending on time chosen
  handleChangeTimeSelection = values => {
    this.setState({ timeSelection: values.length ? values[0] : null });
  }

  // Function to change component shown between chart and table
  handleChangeChartType = values => {
    this.setState({ chartType: values.length ? values[0] : null });
  }

  componentDidMount(){
    // Upon component mounting, refresh the table once to show latest data
    const players = this.props.data
    for (let key in players){
      this.refreshTableData(key)
    }
  }

  render() {
    const { timeSelection, chartType, tableData} = this.state;
    const isSpecificTime = timeSelection === this.timeOptions[2];
    const key = this.props.match.params.id
    const player = this.props.data[key]
    let valMax:number = player.timeData.length>0 ? (player.timeData[player.timeData.length-1]):10
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
            {chartType.value===this.chartOptions[0].value?
            <div>
              {player.timeData.length ?
                <LineChart
                  timeData={player.timeData}
                  peopleCount={player.peopleCount}
                  valMax={valMax}
                />
                :
                <h2>No data to display</h2>
              }

            </div>
            :
            <div>
              <Table data={tableData[key]} refreshTable={this.refreshTableData} id={key} />
            </div>
            }
          </div>
        </div>
      </div>
    );
  }
}

export default Analysis;
