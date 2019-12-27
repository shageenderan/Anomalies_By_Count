import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from "react-router-dom";

// Components
import SideBar from './components/SideBar/Sidebar';

import { makeStyles } from '@material-ui/core/styles';
import Cameras from './components/Cameras/Cameras';
import Analysis from './components/Analysis/Analysis';


function Home(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <Cameras></Cameras>
    </div>
  )
}

function Stats(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Stats here</h1>
    </div>
  )
}

function AnalysisPage(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <Analysis></Analysis>
    </div>
  )
}

function Playback(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Playback here</h1>
    </div>
  )
}

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
  },
  content: {
    marginLeft: '10px',
  },
}));

const App: React.FC = () => {
  const classes = useStyles();
  return (
    <div className="App">
      <Router>
        <div className={classes.root}>
          <SideBar />
          <Route exact path="/" component={Home} />

          <Route path="/cameras" component={Home} />

          <Route path="/stats" component={Stats} />

          <Route path="/analysis" component={AnalysisPage} />

          <Route path="/playback" component={Playback} />
        </div>
      </Router>
    </div>
  );
}

export default App;
