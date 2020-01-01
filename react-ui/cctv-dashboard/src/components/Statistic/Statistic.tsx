import React, { Component } from "react";
import Chart from "./Charts/StatisticChart";

class Statistic extends Component {
  state = {
    charts: {
      // Hard code the statistic data for now
      1: {
        show: true,
        text: "Camera 1",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0],
        maximise: false
      },
      2: {
        show: true,
        text: "Camera 2",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0],
        maximise: false
      },
      3: {
        show: true,
        text: "Camera 3",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0],
        maximise: false
      },
      4: {
        show: true,
        text: "Camera 4",
        timeData: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        peopleCount: [0, 53, 75, 24, 70, 321, 43, 234, 26, 0],
        maximise: false
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
      } else {
        charts[key].maximise = !charts[key].maximise;
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
          maximise={charts[key].maximise}
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
