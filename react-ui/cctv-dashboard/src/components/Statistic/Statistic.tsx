import React, { Component } from "react";
import Chart from "./Charts/LineChart";

class Statistic extends Component {
  state = {
    charts: {
      // Hard cord the statistic data for now
      1: {
        show: true,
        text: "Camera 1",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0]
      },
      2: {
        show: true,
        text: "Camera 2",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0]
      },
      3: {
        show: true,
        text: "Camera 3",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0]
      },
      4: {
        show: true,
        text: "Camera 4",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0]
      }
    },
    showNav: false
  };
  click = id => {
    const charts = Object.create(this.state.charts);
    let showNav = false;
    for (let key in this.state.charts) {
      if (key !== id) {
        charts[key].show = !charts[key].show;
        showNav = !charts[key].show;
      }
    }
    this.setState({ charts, showNav });
  };

  render() {
    const { charts, showNav } = this.state;
    let currentCharts: any = [];
    for (let key in charts) {
      currentCharts.push(
        <Chart
          timeData={charts[key].timeData}
          peopleCount={charts[key].peopleCount}
          key={key}
          id={key}
          text={charts[key].text}
          show={charts[key].show}
          click={this.click}
        />
      );
    }

    return (
      <div className="container-truex">
        <div className="row">{currentCharts}</div>
      </div>
    );
  }
}

export default Statistic;
